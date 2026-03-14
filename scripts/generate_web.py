import json
from jinja2 import Environment, FileSystemLoader

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 处理摘要占位符
            for item in data:
                if not item.get('summary'):
                    raw_abs = item.get('abstract_raw', '')
                    item['summary'] = (raw_abs[:100] + "...") if raw_abs else "暂无摘要，请点击原文查看。"
            return data
    except FileNotFoundError:
        return []

# 加载数据源
s2_papers = load_data("data/s2.json")
pubmed_papers = load_data("data/pubmed.json")
arxiv_papers = load_data("data/arxiv.json")

# 合并并排序
all_papers_combined = s2_papers + pubmed_papers + arxiv_papers
all_papers_combined.sort(key=lambda x: x.get("date", ""), reverse=True)

# 安全加载爬虫状态字典
try:
    with open("data/run_stats.json", "r", encoding="utf-8") as f:
        run_stats = json.load(f)
except FileNotFoundError:
    run_stats = {"total": len(all_papers_combined), "success": len(all_papers_combined), "failed": 0}

# 渲染网页
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index_template.html")
html_content = template.render(all_papers=all_papers_combined, stats=run_stats)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✨ index.html 已生成！目前大盘共收录 {len(all_papers_combined)} 篇文献。")
