import requests
import xmltodict
import json
from datetime import datetime, timedelta

# ========================
# 配置查询关键词
# ========================
QUERY = "deep learning OR LLM OR agent OR fine-tuning"
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")

# PubMed E-Utilities URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
ESearch_URL = f"{BASE_URL}esearch.fcgi?db=pubmed&term={QUERY}&reldate=1&retmode=json"
Efetch_URL = f"{BASE_URL}efetch.fcgi?db=pubmed&retmode=xml&id="

papers = []

try:
    # 1️⃣ 获取文献 ID
    res = requests.get(ESearch_URL, timeout=20)
    res.raise_for_status()
    idlist = res.json().get("esearchresult", {}).get("idlist", [])

    if idlist:
        # 2️⃣ 获取文献详细信息
        fetch_res = requests.get(Efetch_URL + ",".join(idlist), timeout=20)
        fetch_res.raise_for_status()
        doc = xmltodict.parse(fetch_res.text)

        articles = doc.get("PubmedArticleSet", {}).get("PubmedArticle", [])
        if not isinstance(articles, list):
            articles = [articles]  # 保证是列表

        for article in articles:
            medline = article.get("MedlineCitation", {}).get("Article", {})
            title = medline.get("ArticleTitle", "")

            # 作者列表
            authors_list = medline.get("AuthorList", {}).get("Author", [])
            authors = []
            if isinstance(authors_list, list):
                for author in authors_list[:3]:  # 只取前三位
                    last = author.get("LastName", "")
                    fore = author.get("ForeName", "")
                    authors.append(f"{fore} {last}".strip())
            elif isinstance(authors_list, dict):
                last = authors_list.get("LastName", "")
                fore = authors_list.get("ForeName", "")
                authors.append(f"{fore} {last}".strip())

            # 日期
            date = medline.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", YESTERDAY)

            # PubMed 链接
            pmid = article.get("MedlineCitation", {}).get("PMID", {}).get("#text", "")
            link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

            papers.append({
                "title": title,
                "authors": authors,
                "link": link,
                "date": date
            })

except requests.RequestException as e:
    print(f"PubMed fetch failed: {e}")

except Exception as e:
    print(f"Unexpected error parsing PubMed data: {e}")

# 保存 JSON
with open("data/pubmed.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)

print(f"PubMed: {len(papers)} papers fetched.")
