import requests
import json
import time
import os
import re
from datetime import datetime, timedelta, timezone

QUERY = '"protein language model" | "virtual drug screening" | "virtual screening" | "ADMET" | "drug discovery" | "molecular docking" | "deep learning" | "large language model"'
URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

today = datetime.now(timezone.utc)
start_date = today - timedelta(days=15)
# 本地保留数据的时间放宽到 15 天
cutoff_date = today - timedelta(days=15)
date_range = f"{start_date.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

api_key = os.environ.get("S2_API_KEY") 
if api_key:
    headers["x-api-key"] = api_key

all_papers_dict = {} 
TAG_KEYWORDS = ["Deep Learning", "LLM", "Foundation Model", "Agent", "Fine-tuning", "Protein Language Model"]

print("开始基于官方 Bulk API 的高效合并抓取...")
stats_total = 0

# 构建请求参数，bulk 终点同样支持 sort 排序
params = {
    "query": QUERY,
    "publicationDateOrYear": date_range,
    "fields": "title,authors,url,publicationDate,citationCount,venue,publicationTypes,abstract,externalIds",
    "sort": "publicationDate:desc"
}

max_retries = 3
for attempt in range(max_retries):
    try:
        # 强制休息 2 秒，保护 API
        time.sleep(2) 
        response = requests.get(URL, params=params, headers=headers, timeout=30)
        
        if response.status_code == 429:
            wait = (attempt + 1) * 5
            print(f"   ⚠️ 触发限流，等待 {wait} 秒...")
            time.sleep(wait)
            continue
            
        response.raise_for_status()
        data = response.json()
        
        items = data.get("data", [])
        stats_total += len(items)
        print(f"Bulk API 成功返回 {len(items)} 篇文献。")
        
        # 解析并清洗数据
        for item in items:
            paper_id = item.get("paperId")
            pub_date_str = item.get("publicationDate")
            
            # 时间过滤
            if not pub_date_str:
                continue
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if pub_date < cutoff_date:
                    continue # 太老的数据，跳过
            except ValueError:
                continue
            
            if paper_id and paper_id not in all_papers_dict:
                title = item.get("title", "")
                title_lower = title.lower()
                
                # 将标题和摘要合并，转换为小写，用于进行更深度的关键词扫描
                abstract_lower = (item.get("abstract", "") or "").lower()
                content_lower = title_lower + " " + abstract_lower
                matched_keywords = []
                
                # 1. 基础标签 (修复 Agent 匹配 reagent 的问题，兼容连字符和空格，兼容复数)
                if re.search(r'\bdeep learning\b', title_lower):
                    matched_keywords.append("Deep Learning")
                if re.search(r'\bfoundation models?\b', title_lower):
                    matched_keywords.append("Foundation Model")
                if re.search(r'\bagents?\b', title_lower): # 完美避开 reagents
                    matched_keywords.append("Agent")
                if re.search(r'\bfine[- ]tuning\b', title_lower): # 兼容 fine-tuning 和 fine tuning
                    matched_keywords.append("Fine-tuning")
                
                # 定义通用高频词的正则状态，避免后续重复计算,兼容 large language model(s) 和 llm(s)
                has_llm = bool(re.search(r'\b(large language models?|llms?)\b', content_lower))

                # 2. PLM 专属逻辑
                has_protein = bool(re.search(r'\bproteins?\b', content_lower))
                has_plm = bool(re.search(r'\bprotein language models?\b', content_lower))
                if has_plm or (has_protein and has_llm):
                    matched_keywords.append("Protein Language Model")

                # 3. BLM 专属逻辑
                has_nucleic_acid = bool(re.search(r'\b(gene|genes|dna|rna|genome|genomics|nucleotide)\b', content_lower))
                if has_nucleic_acid and has_llm:
                    matched_keywords.append("Biological Large Model")
                    
                # 4. AIDD 专属逻辑 (修复短字母缩写误伤，兼容格式)
                has_ai_algo = bool(re.search(r'\b(deep learning|gnns?|machine learning|artificial intelligence)\b', content_lower))
                has_drug_task = bool(re.search(r'\b(virtual screening|admet|drug[- ]likeness|drug discovery|molecular docking)\b', content_lower))
                if has_ai_algo and has_drug_task:
                    matched_keywords.append("AIDD")

                valid_core_tags = {"Protein Language Model", "Biological Large Model", "AIDD"}
                if not any(tag in valid_core_tags for tag in matched_keywords):
                    continue  # 不满足条件，直接丢弃这篇文章，跳过本次循环！
                # 确认是硬核文章后，再打上近三天标签（修正了之前的重复 Bug）
                diff_days = (today - pub_date).days
                if diff_days <= 3:
                    matched_keywords.append("🆕 近三天更新")
                    
                authors_raw = item.get("authors", [])
                authors = [a.get("name") for a in authors_raw[:3] if a.get("name")]
                if len(authors_raw) > 3:
                    authors.append("et al.")
                    
                citations = item.get("citationCount", 0)
                venue = item.get("venue", "")
                doi = item.get("externalIds", {}).get("DOI", "") if item.get("externalIds") else ""
                
                if citations > 0:
                    matched_keywords.append(f"Cited: {citations}")
                
                # 交叉验证，防止 API 错误地将作者名识别为期刊名
                if venue:
                    venue_clean = venue.strip()
                    venue_lower = venue_clean.lower()
                    is_author_name = False
                    
                    for a in authors_raw:
                        name = a.get("name", "").lower().strip()
                        if not name:
                            continue
                        if venue_lower == name or (len(name) > 4 and name in venue_lower):
                            is_author_name = True
                            break
                            
                    if not is_author_name:
                        matched_keywords.append(venue_clean)
                        
                all_papers_dict[paper_id] = {
                    "title": title,
                    "authors": authors,
                    "link": item.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}",
                    "date": pub_date_str,
                    "keywords": matched_keywords,
                    "source": "Semantic Scholar",
                    "abstract_raw": item.get("abstract", ""),
                    "summary": "",
                    "doi": doi,
                    "citations": citations
                }
        
        # 因为已经把所有查询合并为一次请求，只要成功就可以直接跳出重试循环
        break 
        
    except requests.exceptions.RequestException as e:
        print(f"   请求失败: {e}")
        if attempt == max_retries - 1:
            print("   抓取失败，放弃当前请求。")

# 将字典转为列表并按日期倒序排列
final_papers = list(all_papers_dict.values())
final_papers.sort(key=lambda x: x["date"], reverse=True)

# 1. 筛选出“近三天”的文献，并打上时间标签
recent_3days_papers = []
for paper in final_papers:
    try:
        pub_date = datetime.strptime(paper["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        diff_days = (today - pub_date).days
        if diff_days <= 3:
            recent_3days_papers.append(paper)
    except ValueError:
        continue

# 2. 依然保留一份总数据库，防止以后需要查历史数据
with open("data/s2.json", "w", encoding="utf-8") as f:
    json.dump(final_papers, f, ensure_ascii=False, indent=2)

# 3. 核心需求：将这三天的内容，单独保存在一个“专属文献文件夹”中
update_folder = "data/recent_updates"
os.makedirs(update_folder, exist_ok=True) # 如果文件夹不存在会自动创建

date_str = today.strftime('%Y-%m-%d')
archive_path = f"{update_folder}/update_{date_str}.json" # 按日期命名的快照文件

with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(recent_3days_papers, f, ensure_ascii=False, indent=2)

# 4. 单独存一份“最新快照”，专门喂给网页生成器使用
with open("data/latest_s2_update.json", "w", encoding="utf-8") as f:
    json.dump(recent_3days_papers, f, ensure_ascii=False, indent=2)

print(f"🎉 抓取完成！共获得 {len(final_papers)} 篇文献，其中近3天更新的 {len(recent_3days_papers)} 篇已独立存档至 {update_folder}。")

# 5. 更新统计数据（让网页上的爬虫报告展示更精确）
run_stats = {
    "total": stats_total,
    "success": len(final_papers),           # 15天总库的数量
    "new_added": len(recent_3days_papers),  # 本次（3天内）新增的数量
    "failed": stats_total - len(final_papers) 
}
with open("data/run_stats.json", "w", encoding="utf-8") as f:
    json.dump(run_stats, f, ensure_ascii=False, indent=2)
