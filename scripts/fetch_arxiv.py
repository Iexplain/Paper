import feedparser
import json
from datetime import datetime, timedelta

# 设置关键词和数量
QUERY = "deep learning OR LLM OR agent OR fine-tuning"
MAX_RESULTS = 10

# 获取最近一天的文献
yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime("%Y%m%d")

url = f"http://export.arxiv.org/api/query?search_query=all:{QUERY}&start=0&max_results={MAX_RESULTS}&sortBy=submittedDate&sortOrder=descending"

feed = feedparser.parse(url)

papers = []
for entry in feed.entries:
    published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
    if published_date.date() == yesterday.date():
        papers.append({
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "link": entry.link,
            "date": published_date.strftime("%Y-%m-%d")
        })

with open("data/arxiv.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)

print(f"ArXiv: {len(papers)} papers fetched.")
