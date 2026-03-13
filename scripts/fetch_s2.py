import requests
import json
from datetime import datetime, timedelta, timezone

# 组合关键词 (S2 的搜索非常强大，直接用空格和 OR 即可)
QUERY = "deep learning OR LLM OR foundation model OR agent OR fine-tuning OR protein language model"

# S2 API 端点
URL = "https://api.semanticscholar.org/graph/v1/paper/search"

# 设定时间窗口：为了弥补 S2 的收录延迟，我们拉取过去 3 天的数据
today = datetime.now(timezone.utc)
three_days_ago = today - timedelta(days=3)
date_range = f"{three_days_ago.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

params = {
    "query": QUERY,
    "publicationDateOrYear": date_range,
    # 一次性要求返回：标题、作者、链接、日期、引用数、期刊名、文章类型、原文摘要
    "fields": "title,authors,url,publicationDate,citationCount,venue,publicationTypes,abstract",
    "limit": 100,
    "sort": "publicationDate:desc"
}

print(f"Fetching from Semantic Scholar API...")
try:
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    papers = []
    TAG_KEYWORDS = ["Deep Learning", "LLM", "Foundation Model", "Agent", "Fine-tuning", "Protein Language Model"]

    for item in data.get("data", []):
        title = item.get("title", "")
        
        # 1. 提取基础 Tag
        matched_keywords = [kw for kw in TAG_KEYWORDS if kw.lower() in title.lower()]

        # 2. 提取并清洗作者信息 (最多保留3位)
        authors_raw = item.get("authors", [])
        authors = [a.get("name") for a in authors_raw[:3]]
        if len(authors_raw) > 3:
            authors.append("et al.")

        # 3. 🌟 添加高价值标签：引用量与期刊名
        citations = item.get("citationCount", 0)
        venue = item.get("venue", "")
        if citations > 0:
            matched_keywords.append(f"🔥 Cited: {citations}")
        if venue:
            matched_keywords.append(f"📓 {venue}")

        papers.append({
            "title": title,
            "authors": authors,
            # 如果没有官方 URL，使用 S2 自己的详情页兜底
            "link": item.get("url") or f"https://www.semanticscholar.org/paper/{item.get('paperId')}",
            "date": item.get("publicationDate", ""),
            "keywords": matched_keywords,
            "source": "Semantic Scholar",
            # 🌟 直接拿到原文摘要，留给后续的 AI Agent 使用
            "abstract_raw": item.get("abstract", ""),
            "summary": "" # 预留给中文 AI 简述的字段
        })

    # 保存为统一的 s2.json
    with open("data/s2.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"✅ Semantic Scholar: {len(papers)} papers fetched.")

except Exception as e:
    print(f"❌ Failed to fetch from Semantic Scholar: {e}")
