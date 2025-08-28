
from textnode import TextNode, TextType

from extractmarkdown import extract_markdown_images, extract_markdown_links

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

def split_nodes_image(old_nodes):
    new_node_list = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_node_list.append(n)
        else:
            image_match = extract_markdown_images(n.text)
            original_text = n.text
            if not image_match:
                new_node_list.append(n)
                continue
            for i in range(len(image_match)):
                image_alt = image_match[i][0]
                image_link = image_match[i][1]
                left,right = original_text.split(f"![{image_alt}]({image_link})",1)
                original_text = right   
                if left:    
                    new_node_text =TextNode(left,TextType.TEXT)
                    new_node_list.append(new_node_text)
                image_node = TextNode(image_alt,TextType.IMAGE,image_link)
                new_node_list.append(image_node)
            if original_text:
                final_text = TextNode(original_text,TextType.TEXT)
                new_node_list.append(final_text)
    return new_node_list

def split_nodes_link(old_nodes):
    new_node_list = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_node_list.append(n)
        else:
            link_match = extract_markdown_links(n.text)
            original_text = n.text
            if not link_match:
                new_node_list.append(n)
                continue
            for i in range(len(link_match)):
                link_alt = link_match[i][0]
                link_url = link_match[i][1]
                left,right = original_text.split(f"[{link_alt}]({link_url})",1)
                original_text = right   
                if left:    
                    new_node_text =TextNode(left,TextType.TEXT)
                    new_node_list.append(new_node_text)
                link_node = TextNode(link_alt,TextType.LINK,link_url)
                new_node_list.append(link_node)
            if original_text:
                final_text = TextNode(original_text,TextType.TEXT)
                new_node_list.append(final_text)
    return new_node_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    output_list = []
    bold_result = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_result = split_nodes_delimiter(bold_result, "_", TextType.ITALIC)
    code_result = split_nodes_delimiter(italic_result, "`", TextType.CODE)
    image_result = split_nodes_image(code_result)
    link_result = split_nodes_link(image_result)
    output_list.extend(link_result)
    return output_list