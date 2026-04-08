from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from textnode import TextNode,text_node_to_html_node,TextType
from inline_markdown import text_to_textnode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n"," ")
            block_node = ParentNode(tag="p",children = text_to_children(block))
            block_nodes.append(block_node)
        elif block_type ==  BlockType.HEADING:
            h_count = 0
            for i in range(6):
                if block[i] == "#":
                    h_count += 1
            block_node = ParentNode(tag=f"h{h_count}",children = text_to_children(block[h_count+1:]))
            block_nodes.append(block_node)
        elif block_type == BlockType.CODE:
            child_node = text_node_to_html_node(TextNode(block[4:len(block)-3],TextType.CODE))
            block_node = ParentNode(tag="pre",children = [child_node])
            block_nodes.append(block_node)
        elif block_type == BlockType.QUOTE:
            if block[1] == " ":
                block = block[2:]
            else:
                block = block[1:]
            block_node = ParentNode(tag="blockquote",children  = text_to_children(block))
            block_nodes.append(block_node)
        elif block_type == BlockType.ULIST:
            list_nodes = []
            items = block.split("\n")
            for item in items:
                list_node = ParentNode(tag="li",children = text_to_children(item[2:]))
                list_nodes.append(list_node)
            block_node = ParentNode(tag="ul",children  = list_nodes)
            block_nodes.append(block_node)
        elif block_type == BlockType.OLIST:
            list_nodes = []
            items = block.split("\n")
            for item in items:
                list_node = ParentNode(tag="li",children = text_to_children(item[3:]))
                list_nodes.append(list_node)
            block_node = ParentNode(tag="ol",children  = list_nodes)
            block_nodes.append(block_node)

    return ParentNode(tag = "div", children = block_nodes)



def text_to_children(text):
    text_nodes = text_to_textnode(text)
    return [text_node_to_html_node(node) for node in text_nodes]



