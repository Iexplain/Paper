import json
from jinja2 import Environment, FileSystemLoader

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 模拟：如果没有摘要，截取原文摘要或占位
            for item in data:
                if 'summary' not in item or not item['summary']:
                    item['summary'] = "本论文探讨了领域内的前沿技术，重点优化了模型性能..." # 实际应由AI生成
            return data
    except FileNotFoundError:
        return []

# 加载数据
arxiv = load_data("data/arxiv.json")
pubmed = load_data("data/pubmed.json")

# 设置 Jinja2 模板
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index_template.html")

# 渲染并保存
html_content = template.render(arxiv=arxiv, pubmed=pubmed)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✨ 现代化的 index.html 已生成！")
