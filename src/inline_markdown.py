from textnode import TextNode, TextType

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





