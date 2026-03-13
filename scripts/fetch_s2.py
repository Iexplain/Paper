import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone

# 组合关键词
QUERY = "deep learning OR LLM OR foundation model OR agent OR fine-tuning OR protein language model"
URL = "https://api.semanticscholar.org/graph/v1/paper/search"

today = datetime.now(timezone.utc)
three_days_ago = today - timedelta(days=3)
date_range = f"{three_days_ago.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

params = {
    "query": QUERY,
    "publicationDateOrYear": date_range,
    "fields": "title,authors,url,publicationDate,citationCount,venue,publicationTypes,abstract",
    "limit": 50,  # 稍微调低单次请求量，降低被封禁的概率
    "sort": "publicationDate:desc"
}

# 🌟 核心防御 1：伪装头与 API Key 预留
headers = {
    # 告诉服务器我们是个正经浏览器/应用，而不是恶意脚本
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# 如果你未来去 S2 官网申请了免费的 API Key，可以通过环境变量 S2_API_KEY 传入
api_key = os.environ.get("S2_API_KEY")
if api_key:
    headers["x-api-key"] = api_key

print(f"Fetching from Semantic Scholar API...")

# 🌟 核心防御 2：工业级重试机制 (Exponential Backoff)
max_retries = 3
data = None

for attempt in range(max_retries):
    try:
        response = requests.get(URL, params=params, headers=headers, timeout=30)
        
        if response.status_code == 429:
            wait_time = (attempt + 1) * 5  # 遇到 429，分别等待 5秒、10秒、15秒后再试
            print(f"⚠️ 触发限流 (429)，等待 {wait_time} 秒后重试 (第 {attempt + 1}/{max_retries} 次)...")
            time.sleep(wait_time)
            continue
            
        response.raise_for_status()
        data = response.json()
        break # 成功则跳出循环
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        if attempt == max_retries - 1:
            print("🚨 达到最大重试次数，放弃抓取。")
            exit(1)
        time.sleep(2)

if data:
    papers = []
    TAG_KEYWORDS = ["Deep Learning", "LLM", "Foundation Model", "Agent", "Fine-tuning", "Protein Language Model"]

    for item in data.get("data", []):
        title = item.get("title", "")
        matched_keywords = [kw for kw in TAG_KEYWORDS if kw.lower() in title.lower()]

        authors_raw = item.get("authors", [])
        authors = [a.get("name") for a in authors_raw[:3]]
        if len(authors_raw) > 3:
            authors.append("et al.")

        citations = item.get("citationCount", 0)
        venue = item.get("venue", "")
        if citations > 0:
            matched_keywords.append(f"🔥 Cited: {citations}")
        if venue:
            matched_keywords.append(f"📓 {venue}")

        papers.append({
            "title": title,
            "authors": authors,
            "link": item.get("url") or f"https://www.semanticscholar.org/paper/{item.get('paperId')}",
            "date": item.get("publicationDate", ""),
            "keywords": matched_keywords,
            "source": "Semantic Scholar",
            "abstract_raw": item.get("abstract", ""),
            "summary": "" 
        })

    with open("data/s2.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"✅ Semantic Scholar: {len(papers)} papers fetched successfully.")
