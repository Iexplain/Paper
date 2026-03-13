import requests
import xmltodict
import json
from datetime import datetime, timedelta

# 查询关键词
QUERY = "deep learning OR LLM OR agent OR fine-tuning"
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")

# PubMed E-Utilities
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
ESearch_URL = f"{BASE_URL}esearch.fcgi?db=pubmed&term={QUERY}&reldate=1&retmode=json"
Efetch_URL = f"{BASE_URL}efetch.fcgi?db=pubmed&retmode=xml&id="

# 1. 获取文献 ID
res = requests.get(ESearch_URL)
ids = res.json()["esearchresult"]["idlist"]

if not ids:
    papers = []
else:
    # 2. 获取详细文献信息
    fetch_res = requests.get(Efetch_URL + ",".join(ids))
    doc = xmltodict.parse(fetch_res.text)
    papers = []
    for article in doc["PubmedArticleSet"]["PubmedArticle"]:
        medline = article["MedlineCitation"]["Article"]
        title = medline.get("ArticleTitle", "")
        authors_list = medline.get("AuthorList", {}).get("Author", [])
        authors = []
        if isinstance(authors_list, list):
            for author in authors_list[:3]:  # 只取前三位
                last = author.get("LastName", "")
                fore = author.get("ForeName", "")
                authors.append(f"{fore} {last}")
        elif isinstance(authors_list, dict):
            last = authors_list.get("LastName", "")
            fore = authors_list.get("ForeName", "")
            authors.append(f"{fore} {last}")

        date = medline.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", YESTERDAY)
        papers.append({
            "title": title,
            "authors": authors,
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']['#text']}/",
            "date": date
        })

with open("data/pubmed.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)

print(f"PubMed: {len(papers)} papers fetched.")
