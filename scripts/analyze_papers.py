#!/usr/bin/env python3
import json
import sqlite3
import pandas as pd
from datetime import datetime
import os

def load_papers():
    """加载今日文献"""
    papers_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'papers.json')
    with open(papers_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def enrich_analysis(papers):
    """模拟AI分析：关键词提取、分类、影响力评分"""
    for paper in papers:
        # 关键词提取（实际可接Deepseek API）
        keywords = ['Transformer', 'LLM', 'Attention']  # 简化示例
        paper['keywords'] = keywords[:3]
        paper['category'] = 'NLP/ML' if 'Transformer' in paper['title'] else 'General'
        paper['influence_score'] = paper.get('citations', 0) * 0.7 + len(paper['keywords']) * 10
        paper['summary'] = paper['abstract'][:200] + '...'
    return papers

def update_db_with_analysis(papers):
    """更新数据库分析结果"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'history.db')
    conn = sqlite3.connect(db_path)
    for paper in papers:
        conn.execute('''UPDATE papers SET 
                       keywords=?, category=?, influence_score=?, summary=?
                       WHERE id=?''',
                    (str(paper['keywords']), paper['category'],
                     paper['influence_score'], paper['summary'], paper['id']))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    papers = load_papers()
    enriched = enrich_analysis(papers)
    
    # 保存增强数据（供网页使用）
    enhanced_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'papers_enhanced.json')
    with open(enhanced_path, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    
    update_db_with_analysis(enriched)
    print(f"✅ Analyzed {len(enriched)} papers -> data/papers_enhanced.json")
