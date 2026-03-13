import feedparser
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

# ========================
# 配置查询关键词和抓取数量
# ========================
# 组合英文学术检索词，使用双引号确保词组精确匹配
QUERY = '("deep learning" OR "large language model" OR LLM OR "foundation model" OR agent OR "fine-tuning" OR "protein language model")'
QUERY_ENCODED = quote(QUERY)  
MAX_RESULTS = 100  # 保持 100，确保高频关键词下不会漏掉文章

now_utc = datetime.now(timezone.utc)
past_24h = now_utc - timedelta(hours=24)

url = (
    f"http://export.arxiv.org/api/query?"
    f"search_query=all:{QUERY_ENCODED}"
    f"&start=0&max_results={MAX_RESULTS}"
    f"&sortBy=submittedDate&sortOrder=descending"
)

print(f"Fetching arXiv papers from URL: {url}")
feed = feedparser.parse(url)

papers = []
# 用于给前端卡片打标签的关键词库
TAG_KEYWORDS = ["Deep Learning", "LLM", "Large Language Model", "Foundation Model", "Agent", "Fine-tuning", "Protein Language Model"]

for entry in feed.entries:
    # 只要标题里包含我们的标签词，就自动提取为前端 Tag
    matched_keywords = [kw for kw in TAG_KEYWORDS if kw.lower() in entry.title.lower()]
    
    published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    
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
