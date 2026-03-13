#!/usr/bin/env python3
import arxiv
import scholarly
import json
import sqlite3
import argparse
from datetime import datetime
import os

def init_db():
    """初始化历史数据库[2]"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'history.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS papers 
                    (id TEXT PRIMARY KEY, title TEXT, authors TEXT, date TEXT, 
                     abstract TEXT, pdf_url TEXT, citations INTEGER, UNIQUE(id))''')
    conn.commit()
    return conn

def fetch_arxiv_papers(keywords, max_papers=30):
    """arXiv API搜集（今日20260313后新文优先）"""
    search = arxiv.Search(
        query=f'all:{keywords} AND submittedDate:[20260101 TO 20260313]',
        max_results=max_papers,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        papers.append({
            'id': result.entry_id.split('/')[-1],
            'title': result.title,
            'authors': [a.name for a in result.authors],
            'date': str(result.published),
            'abstract': result.summary,
            'pdf_url': result.pdf_url,
            'citations': 0  # arXiv无引用，待分析补充
        })
    return papers

def fetch_google_scholar(keywords, max_papers=10):
    """补充Google Scholar高引论文"""
    search_query = scholarly.search_pubs(keywords)
    papers = []
    for i, result in enumerate(search_query):
        if i >= max_papers: break
        papers.append({
            'id': f'scholar_{i}',
            'title': result['bib']['title'],
            'authors': result.get('bib', {}).get('author', []),
            'date': result.get('bib', {}).get('pub_year', 'N/A'),
            'abstract': result.get('eprint_url', ''),
            'pdf_url': result.get('eprint_url', ''),
            'citations': result.get('num_citations', 0)
        })
    return papers

def save_papers(papers):
    """保存JSON + 增量入库"""
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'papers.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    conn = init_db()
    for paper in papers:
        try:
            conn.execute('''INSERT OR IGNORE INTO papers 
                           (id, title, authors, date, abstract, pdf_url, citations)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (paper['id'], paper['title'], str(paper['authors']),
                         paper['date'], paper['abstract'], paper['pdf_url'],
                         paper['citations']))
        except Exception as e:
            print(f"Skip duplicate: {paper['id']}")
    conn.commit()
    conn.close()
    print(f"✅ Collected {len(papers)} papers saved to data/papers.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', default="Transformer LLM")
    parser.add_argument('--max_papers', type=int, default=30)
    args = parser.parse_args()
    
    all_papers = fetch_arxiv_papers(args.keywords, args.max_papers//2)
    all_papers += fetch_google_scholar(args.keywords, args.max_papers//2)
    
    # 去重
    unique_papers = []
    seen_ids = set()
    for p in all_papers:
        if p['id'] not in seen_ids:
            unique_papers.append(p)
            seen_ids.add(p['id'])
    
    save_papers(unique_papers)
