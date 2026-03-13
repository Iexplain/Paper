#!/usr/bin/env python3
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
import os

def load_data():
    """加载分析后数据"""
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'papers_enhanced.json'), 'r') as f:
        return json.load(f)

def create_charts(papers):
    """生成Plotly交互图表"""
    df = pd.DataFrame(papers)
    
    # 1. 引用热图
    fig1 = px.bar(df, x='title', y='citations', 
                  title='今日高引论文 Top 10',
                  color='influence_score')
    
    # 2. 关键词词云基础（柱状）
    keyword_df = df.explode('keywords')[['keywords', 'influence_score']].groupby('keywords').sum().reset_index()
    fig2 = px.treemap(keyword_df, path=['keywords'], values='influence_score',
                      title='关键词影响力分布')
    
    # 3. 时间线
    df['date'] = pd.to_datetime(df['date'])
    fig3 = px.line(df, x='date', y='influence_score', 
                   title='每日文献影响力趋势')
    
    # 保存JS图表
    figs = [fig1, fig2, fig3]
    for i, fig in enumerate(figs):
        fig.write_html(os.path.join(os.path.dirname(__file__), '..', 'output', 'assets', f'chart_{i+1}.html'))

def render_html(papers):
    """Jinja2渲染主页面"""
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..')))
    template = env.get_template('templates/index.html.j2')
    
    html_content = template.render({
        'papers': papers[:20],  # 前20篇卡片展示
        'total_count': len(papers),
        'update_date': '2026-03-13',  # 动态替换
        'charts': ['chart_1.html', 'chart_2.html', 'chart_3.html']
    })
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'index.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 复制静态资源
    import shutil
    shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'output', 'style.css'), 
                os.path.join(os.path.dirname(__file__), '..', 'output'))
    print("✅ Generated visualization dashboard -> output/index.html")

if __name__ == "__main__":
    papers = load_data()
    create_charts(papers)
    render_html(papers)
