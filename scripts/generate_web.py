import json
from jinja2 import Environment, FileSystemLoader

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 临时占位：如果 summary 为空，先拿 S2 原文摘要的前100个字符顶一下
            for item in data:
                if not item.get('summary'):
                    raw_abs = item.get('abstract_raw', '')
                    item['summary'] = (raw_abs[:100] + "...") if raw_abs else "暂无摘要，请点击原文查看。"
            return data
    except FileNotFoundError:
        return []

# 只加载 S2 的数据
s2_papers = load_data("data/s2.json")

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index_template.html")

# 渲染时只需把 s2_papers 传进去（前端你可以把 pubmed 和 arxiv 的变量全换成 s2_papers）
html_content = template.render(all_papers=s2_papers)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✨ 现代化的 index.html 已生成！")
