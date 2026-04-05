from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node_texts = old_node.text.split(delimiter)
        if len(split_node_texts) % 2 == 0:
            raise ValueError(f"invalid markdown syntax, missing closing {delimiter}")
        for i,text in enumerate(split_node_texts):
            if i % 2 == 0:
                new_nodes.append(TextNode(text,TextType.TEXT))
            else:
                new_nodes.append(TextNode(text,text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_images = extract_markdown_images(old_node.text) 
        non_matches = re.split(r"!\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)",old_node.text)
        for i in range(len(non_matches)+len(node_images)):
            if i % 2 == 0:
                if len(non_matches[i//2])>0:
                    new_nodes.append(TextNode(non_matches[i//2], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_images[(i-1)//2][0],TextType.IMAGE, node_images[(i-1)//2][1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_links = extract_markdown_links(old_node.text) 
        non_matches = re.split(r"(?<!!)\[(?:[^\[\]]*)\]\((?:[^\(\)]*)\)",old_node.text)
        for i in range(len(non_matches)+len(node_links)):
            if i % 2 == 0:
                if len(non_matches[i//2])>0:
                    new_nodes.append(TextNode(non_matches[i//2], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_links[(i-1)//2][0],TextType.LINK, node_links[(i-1)//2][1]))
    return new_nodes

