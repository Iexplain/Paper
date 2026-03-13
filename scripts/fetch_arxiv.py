import feedparser
import json
from datetime import datetime, timedelta
from urllib.parse import quote

# ========================
# 配置查询关键词和抓取数量
# ========================
QUERY = "deep learning OR LLM OR agent OR fine-tuning"
QUERY_ENCODED = quote(QUERY)  # 对空格和特殊字符进行 URL encode
MAX_RESULTS = 10

# 获取昨天日期
yesterday = datetime.now() - timedelta(days=1)
yesterday_date = yesterday.date()

# 构建 arXiv API URL
url = (
    f"http://export.arxiv.org/api/query?"
    f"search_query=all:{QUERY_ENCODED}"
    f"&start=0&max_results={MAX_RESULTS}"
    f"&sortBy=submittedDate&sortOrder=descending"
)

print(f"Fetching arXiv papers from URL: {url}")

# 解析 RSS feed
feed = feedparser.parse(url)

# 筛选昨天的文献
papers = []
for entry in feed.entries:
    keywords = ["LLM", "Deep Learning", "Agent", "Fine-tuning"]  # 可自定义
    matched_keywords = [kw for kw in keywords if kw.lower() in entry.title.lower()]
    published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
    if published_date.date() == yesterday_date:
        authors_list = [author.name for author in entry.authors]
        if len(authors_list) > 3:
            authors_list = authors_list[:3] + ["et al."]
        papers.append({
            "title": entry.title.strip(),
            "authors": authors_list,
            "link": entry.link,
            "date": published_date.strftime("%Y-%m-%d")
            "keywords": matched_keywords,
            "source": "arXiv"
        })

# 保存 JSON
with open("data/arxiv.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)

print(f"ArXiv: {len(papers)} papers fetched.")
