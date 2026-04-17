import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    markdown = markdown.strip()
    if not markdown.startswith("# "):
        raise ValueError("invalid header")
    return markdown.split("\n")[0][2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template_html = f.read()
    htmlStr = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template_html = template_html.replace("{{ Title }}",title)
    template_html = template_html.replace("{{ Content }}",htmlStr)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_path, 'w') as f:
        f.write(template_html)
