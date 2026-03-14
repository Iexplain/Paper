import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone

# 🌟 优化1：拆分关键词，对 S2 API 更友好
QUERIES = [
    "large language model",
    "foundation model",
    "protein language model",
    "deep learning",
    "fine-tuning"
]

URL = "https://api.semanticscholar.org/graph/v1/paper/search"

# 🌟 优化2：时间窗口放宽到 7 天，防止 API 索引延迟漏数据
today = datetime.now(timezone.utc)
seven_days_ago = today - timedelta(days=7)
# 真正展示在前端的，只取过去 3 天的数据（本地过滤）
cutoff_date = today - timedelta(days=3)

date_range = f"{seven_days_ago.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

# 强烈建议去官网免费申请一个 Key：https://www.semanticscholar.org/product/api
# 申请到后，可以把下面这行的 os.environ.get 替换成你的真实字符串，如 api_key = "你的KEY"
api_key = os.environ.get("S2_API_KEY") 
if api_key:
    headers["x-api-key"] = api_key

all_papers_dict = {} # 用字典来去重 (以 paperId 为 key)
TAG_KEYWORDS = ["Deep Learning", "LLM", "Foundation Model", "Agent", "Fine-tuning", "Protein Language Model"]

print("🚀 开始多线程/多关键词安全抓取...")
stats_total = 0  # 记录 API 返回的文献总数

for query in QUERIES:
    params = {
        "query": query,
        "publicationDateOrYear": date_range,
        # 👇 在末尾加上 ,externalIds
        "fields": "title,authors,url,publicationDate,citationCount,venue,publicationTypes,abstract,externalIds",
        "limit": 30, 
        "sort": "publicationDate:desc"
    }
    
    print(f"👉 正在检索关键词: [{query}] ...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 每次请求前强制休息 2 秒，极大降低 429 概率
            time.sleep(2) 
            response = requests.get(URL, params=params, headers=headers, timeout=20)
            
            if response.status_code == 429:
                wait = (attempt + 1) * 5
                print(f"   ⚠️ 触发限流，等待 {wait} 秒...")
                time.sleep(wait)
                continue
                
            response.raise_for_status()
            data = response.json()
            # 记录每次 API 返回的文献数量
            items = data.get("data", [])
            stats_total += len(items)
            
            # 解析并清洗数据
            for item in data.get("data", []):
                paper_id = item.get("paperId")
                pub_date_str = item.get("publicationDate")
                
                # 🌟 优化3：在本地进行精确的时间过滤（只要最近 3 天的）
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
                    matched_keywords = [kw for kw in TAG_KEYWORDS if kw.lower() in title.lower()]
                    
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
                        matched_keywords.append(f"{venue}")
                        
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
            break # 这个关键词抓取成功，跳出重试循环
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ 请求失败: {e}")
            if attempt == max_retries - 1:
                print("   🚨 放弃当前关键词。")

# 将字典转为列表并按日期倒序排列
final_papers = list(all_papers_dict.values())
final_papers.sort(key=lambda x: x["date"], reverse=True)

# 写入文件
with open("data/s2.json", "w", encoding="utf-8") as f:
    json.dump(final_papers, f, ensure_ascii=False, indent=2)

print(f"🎉 抓取完成！共获得 {len(final_papers)} 篇有效去重文献。")
# 新增：将真实的运行状态保存下来，供网页生成使用
run_stats = {
    "total": stats_total,
    "success": len(final_papers),
    "failed": stats_total - len(final_papers) # 包括太老被过滤的、重复的等
}
with open("data/run_stats.json", "w", encoding="utf-8") as f:
    json.dump(run_stats, f, ensure_ascii=False, indent=2)
