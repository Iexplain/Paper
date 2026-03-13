import feedparser
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

# ========================
# 配置查询关键词和抓取数量
# ========================
QUERY = "deep learning OR LLM OR agent OR fine-tuning"
QUERY_ENCODED = quote(QUERY)  
MAX_RESULTS = 200  # 调大单次查询上限，确保不会漏掉过去24小时内激增的文章

# 核心修改：获取当前 UTC 时间，并划定 24 小时的时间窗口
now_utc = datetime.now(timezone.utc)
past_24h = now_utc - timedelta(hours=24)

# 构建 arXiv API URL
url = (
    f"http://export.arxiv.org/api/query?"
    f"search_query=all:{QUERY_ENCODED}"
    f"&start=0&max_results={MAX_RESULTS}"
    f"&sortBy=submittedDate&sortOrder=descending"
)

print(f"Fetching arXiv papers from URL: {url}")
feed = feedparser.parse(url)

papers = []
for entry in feed.entries:
    keywords = ["LLM", "Deep Learning", "Agent", "Fine-tuning"] 
    matched_keywords = [kw for kw in keywords if kw.lower() in entry.title.lower()]
    
    # 解析 arXiv 的发布时间，并强制指定为 UTC 时区进行精准比对
    published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    
    # 核心判断：只有发布时间落在过去 24 小时内，才会被收录
    if past_24h <= published_date <= now_utc:
        authors_list = [author.name for author in entry.authors]
        if len(authors_list) > 3:
            authors_list = authors_list[:3] + ["et al."]
        papers.append({
            "title": entry.title.strip(),
            "authors": authors_list,
            "link": entry.link,
            "date": published_date.strftime("%Y-%m-%d"),
            "keywords": matched_keywords,
            "source": "arXiv"
        })

with open("data/arxiv.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)

print(f"ArXiv: {len(papers)} papers fetched in the last 24 hours.")
