from enum import Enum
import re
from htmlnode import ParentNode
from textnode import TextNode,text_node_to_html_node,TextType
from inline_markdown import text_to_textnode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return [block for block in blocks if len(block) > 0]

def block_to_block_type(block):
    if re.match(r"^#{1,6} .*",block):
        return BlockType.HEADING
    if re.match(r"^```\n(.*\n?)+```$",block):
        return BlockType.CODE
    if re.match(r"(> ?.*\n?)+",block):
        return BlockType.QUOTE
    if re.match(r"(\- .*\n)+",block):
        return BlockType.ULIST
    if re.match(r"(\d\. .*\n)+",block):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html_node(block):
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p",children)

def heading_to_html_node(block):
    h_count = 0
    for i in range(6):
        if block[i] == "#":
            h_count += 1
    if h_count + 1 >= len(block):
        raise ValueError(f"invalid heading level: {h_count}")
    children = text_to_children(block[h_count+1:])
    return ParentNode(f"h{h_count}",children)

def code_to_html_node(block):
    child_node = text_node_to_html_node(TextNode(block[4:len(block)-3],TextType.CODE))
    children = [child_node]
    return ParentNode("pre",children)

def quote_to_html_node(block):
    if block[1] == " ":
        block = block[2:]
    else:
        block = block[1:]
    children = text_to_children(block)
    return ParentNode("blockquote",children)

def ulist_to_html_node(block):
    children = []
    items = block.split("\n")
    for item in items:
        list_node = ParentNode(tag="li",children = text_to_children(item[2:]))
        children.append(list_node)
    return ParentNode("ul",children)

def olist_to_html_node(block):
    children = []
    items = block.split("\n")
    for item in items:
        list_node = ParentNode(tag="li",children = text_to_children(item[3:]))
        children.append(list_node)
    return ParentNode("ol",children)





