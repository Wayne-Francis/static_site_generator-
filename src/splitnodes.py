
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_node_list.append(n)
        if n.text_type == TextType.TEXT:
            split_text = n.text.split(f"{delimiter}")
            if len(split_text) % 2 == 0:
                raise Exception("invalid Markdown syntax")
            for i in range(len(split_text)):
                piece = split_text[i]
                if piece == "":
                     continue
                if i % 2 == 0:
                    new_node = TextNode(piece,TextType.TEXT)
                    new_node_list.append(new_node)
                else:
                    new_node = TextNode(piece,text_type)
                    new_node_list.append(new_node)
    return new_node_list





