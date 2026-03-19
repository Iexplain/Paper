import requests
import json
import time
import os
import re
from datetime import datetime, timedelta, timezone

# 1. 扁平化 API 检索词，加入 Agent 专属词汇，避免 API 报错
QUERY = '"protein language model" | "virtual screening" | "ADMET" | "drug discovery" | "molecular docking" | "deep learning" | "large language model" | "foundation model" | "AI agent" | "LLM agent" | "autonomous agent"'
URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

# 2. 将保鲜期扩大至 30 天
today = datetime.now(timezone.utc)
start_date = today - timedelta(days=30)
cutoff_date = today - timedelta(days=30)
date_range = f"{start_date.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

api_key = os.environ.get("S2_API_KEY") 
if api_key:
    headers["x-api-key"] = api_key

all_papers_dict = {} 
print("🚀 开始基于官方 Bulk API 的分页流式抓取...")
stats_total = 0

# 构建请求参数，明确要求每次拉满 1000 条
params = {
    "query": QUERY,
    "publicationDateOrYear": date_range,
    "fields": "title,authors,url,publicationDate,citationCount,venue,publicationTypes,abstract,externalIds",
    "sort": "publicationDate:desc",
    "limit": 1000 
}

# 分页控制器
token = None
page_count = 1
max_pages = 10  # 安全阀，最多翻 10 页（捞 10000 条数据）

while page_count <= max_pages:
    if token:
        params["token"] = token # 带上下一页的门票
        
    print(f"正在抓取第 {page_count} 页数据...")
    
    try:
        time.sleep(2) # 保护 API
        response = requests.get(URL, params=params, headers=headers, timeout=30)
        
        if response.status_code == 429:
            print("   ⚠️ 触发限流，等待 10 秒后重试...")
            time.sleep(10)
            continue
            
        response.raise_for_status()
        data = response.json()
        
        items = data.get("data", [])
        if not items:
            break # 没数据了直接跳出
            
        stats_total += len(items)
        print(f"   成功返回 {len(items)} 篇原始文献。")
        
        # 解析并清洗数据
        for item in items:
            paper_id = item.get("paperId")
            pub_date_str = item.get("publicationDate")
            
            # 时间过滤 (本地拦截生死线)
            if not pub_date_str:
                continue
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if pub_date < cutoff_date:
                    continue 
            except ValueError:
                continue
            
            if paper_id and paper_id not in all_papers_dict:
                title = item.get("title", "")
                title_lower = title.lower()
                abstract_lower = (item.get("abstract", "") or "").lower()
                content_lower = title_lower + " " + abstract_lower
                matched_keywords = []
                
                # 提取语境状态
                has_llm = bool(re.search(r'\b(large language models?|llms?)\b', content_lower))
                has_ai_algo = bool(re.search(r'\b(deep learning|gnns?|machine learning|artificial intelligence)\b', content_lower))
                
                # 打基础标签
                if re.search(r'\bdeep learning\b', title_lower):
                    matched_keywords.append("Deep Learning")
                if re.search(r'\bfoundation models?\b', title_lower):
                    matched_keywords.append("Foundation Model")
                
                # Agent 专属打标 (明确的 AI Agent 或 标题有 Agent 且摘要含 AI 算法)
                is_explicit_ai_agent = bool(re.search(r'\b(ai agents?|llm agents?|autonomous agents?|intelligent agents?|multi-agent)\b', content_lower))
                is_title_agent_with_ai = bool(re.search(r'\bagents?\b', title_lower)) and (has_llm or has_ai_algo)
                if is_explicit_ai_agent or is_title_agent_with_ai:
                    matched_keywords.append("Agent")

                # PLM 专属逻辑
                has_protein = bool(re.search(r'\bproteins?\b', content_lower))
                has_plm = bool(re.search(r'\bprotein language models?\b', content_lower))
                if has_plm or (has_protein and has_llm):
                    matched_keywords.append("Protein Language Model")

                # BLM 专属逻辑
                has_nucleic_acid = bool(re.search(r'\b(gene|genes|dna|rna|genome|genomics|nucleotide)\b', content_lower))
                if has_nucleic_acid and has_llm:
                    matched_keywords.append("Biological Large Model")
                    
                # AIDD 专属逻辑
                has_drug_task = bool(re.search(r'\b(virtual screening|admet|drug[- ]likeness|drug discovery|molecular docking)\b', content_lower))
                if has_ai_algo and has_drug_task:
                    matched_keywords.append("AIDD")

                # ==============================================================
                # 🔪 终极海关拦截器：强制 Agent 与生物医药领域的交叉 (AND 关系)
                # ==============================================================
                if "Agent" not in matched_keywords:
                    continue  # 规则 1：必须是 Agent
                    
                domain_tags = {"Protein Language Model", "Biological Large Model", "AIDD"}
                if not any(tag in domain_tags for tag in matched_keywords):
                    continue  # 规则 2：必须应用在咱们生化大模型领域内
                
                # 确认是硬核交叉文章后，判断是否为近 3 天新发
                diff_days = (today - pub_date).days
                if diff_days <= 3:
                    matched_keywords.append("🆕 近三天更新")

                # 获取作者及其他元数据
                authors_raw = item.get("authors", [])
                authors = [a.get("name") for a in authors_raw[:3] if a.get("name")]
                if len(authors_raw) > 3:
                    authors.append("et al.")
                    
                citations = item.get("citationCount", 0)
                venue = item.get("venue", "")
                doi = item.get("externalIds", {}).get("DOI", "") if item.get("externalIds") else ""
                
                if citations > 0:
                    matched_keywords.append(f"Cited: {citations}")
                
                if venue:
                    venue_clean = venue.strip()
                    venue_lower = venue_clean.lower()
                    is_author_name = False
                    for a in authors_raw:
                        name = a.get("name", "").lower().strip()
                        if not name: continue
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
        
        # 翻页判断
        token = data.get("token")
        if not token:
            print("✅ 所有符合条件的数据已彻底抓取完毕！")
            break
            
        page_count += 1
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 请求失败: {e}")
        break 

# 排序
final_papers = list(all_papers_dict.values())
final_papers.sort(key=lambda x: x["date"], reverse=True)

# 1. 筛选出“近三天”的文献（修复了之前的 Double Append Bug）
recent_3days_papers = []
for paper in final_papers:
    try:
        pub_date = datetime.strptime(paper["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        diff_days = (today - pub_date).days
        if diff_days <= 3:
            recent_3days_papers.append(paper)
    except ValueError:
        continue

# 2. 保存 30 天总库
os.makedirs("data", exist_ok=True)
with open("data/s2.json", "w", encoding="utf-8") as f:
    json.dump(final_papers, f, ensure_ascii=False, indent=2)

# 3. 独立存档快照
update_folder = "data/recent_updates"
os.makedirs(update_folder, exist_ok=True)
date_str = today.strftime('%Y-%m-%d')
archive_path = f"{update_folder}/update_{date_str}.json"

with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(recent_3days_papers, f, ensure_ascii=False, indent=2)

# 4. 生成最新快照
with open("data/latest_s2_update.json", "w", encoding="utf-8") as f:
    json.dump(recent_3days_papers, f, ensure_ascii=False, indent=2)

print(f"\n🎉 抓取清洗完成！共捕获 {len(final_papers)} 篇硬核生物智能体文献，其中近3天最新的有 {len(recent_3days_papers)} 篇。")

# 5. 更新统计数据
run_stats = {
    "total": stats_total,
    "success": len(final_papers),
    "new_added": len(recent_3days_papers),
    "failed": stats_total - len(final_papers) 
}
with open("data/run_stats.json", "w", encoding="utf-8") as f:
    json.dump(run_stats, f, ensure_ascii=False, indent=2)
