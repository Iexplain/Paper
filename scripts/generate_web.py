import json
from jinja2 import Environment, FileSystemLoader

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 临时占位：如果 summary 为空，先拿原文摘要的前100个字符顶一下
            for item in data:
                if not item.get('summary'):
                    raw_abs = item.get('abstract_raw', '')
                    item['summary'] = (raw_abs[:100] + "...") if raw_abs else "暂无摘要，请点击原文查看。"
            return data
    except FileNotFoundError:
        return []

# 1. 加载所有来源的数据
s2_papers = load_data("data/s2.json")
pubmed_papers = load_data("data/pubmed.json")
arxiv_papers = load_data("data/arxiv.json")

# 2. 将所有论文合并为一个大列表
all_papers_combined = s2_papers + pubmed_papers + arxiv_papers

# 3. 按日期倒序排列（确保最新抓取的论文永远在最前面）
all_papers_combined.sort(key=lambda x: x.get("date", ""), reverse=True)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index_template.html")

# 4. 把合并后的总数据传给前端模板
html_content = template.render(all_papers=all_papers_combined)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✨ 现代化的 index.html 已生成！目前大盘共收录 {len(all_papers_combined)} 篇文献。")
