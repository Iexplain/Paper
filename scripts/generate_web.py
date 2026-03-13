import json
from jinja2 import Environment, FileSystemLoader

# 读取数据
with open("data/arxiv.json", "r", encoding="utf-8") as f:
    arxiv = json.load(f)

with open("data/pubmed.json", "r", encoding="utf-8") as f:
    pubmed = json.load(f)

# 设置模板
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index_template.html")

# 渲染 HTML
html_content = template.render(arxiv=arxiv, pubmed=pubmed)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html generated.")
