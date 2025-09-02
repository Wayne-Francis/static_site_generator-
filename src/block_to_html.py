from markdown_to_blocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode,TextType, text_node_to_html_node
from splitnodes import text_to_textnodes
import re

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node_ls =[]
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.paragraph:
            block = remove_newline(block)
            children_nodes = text_to_children(block)
            block_html_node = ParentNode(tag= "p", children=children_nodes)
        elif block_type == BlockType.quote:
            block = remove_newline(block)
            block = remove_leading_quote_symbol(block)
            children_nodes = text_to_children(block)
            block_html_node = ParentNode(tag= "blockquote", children=children_nodes)
        elif block_type == BlockType.code:
            block = remove_leading_code_symbol(block)
            code_text_node = TextNode(block, TextType.CODE)
            leaf_node_ls =[]
            leaf_node = text_node_to_html_node(code_text_node)
            leaf_node_ls.append(leaf_node)
            block_html_node = ParentNode(tag= "pre", children=leaf_node_ls)
        elif block_type == BlockType.ordered_list:
            items = remove_leading_numbers_ol(block)
            ls_nodes = []
            for text in items:
                children = text_to_children(text)
                ls_nodes.append(ParentNode(tag= "li", children=children))
            block_html_node = ParentNode(tag= "ol", children=ls_nodes)
        elif block_type == BlockType.unordered_list:
            items = remove_leading_ul(block)
            ls_nodes = []
            for text in items:
                children = text_to_children(text)
                ls_nodes.append(ParentNode(tag= "li", children=children))
            block_html_node = ParentNode(tag= "ul", children=ls_nodes)
        elif block_type == BlockType.heading:
            pairs = strip_headers_count(block)
            level, text = pairs[0]
            children = text_to_children(text)
            block_html_node=ParentNode(tag= f"h{level}", children=children)
        parent_node_ls.append(block_html_node)
    root = ParentNode(tag="div", children=parent_node_ls)
    return root

def strip_headers_count(block):
    split_block = block.split("\n")
    split_list = []
    for item in split_block:
        item = item.strip()
        header_count = 0
        if item == "":
            split_list.append((0,""))
            continue
        for i in range(len(item)):
            if header_count == 6: 
                      break
            if item[i] == "#":
                header_count += 1
            else:
                 break
        if header_count == 0:
            content = item
        elif header_count < len(item):
            if header_count > 0 and item[header_count] == " ":
                content = item[header_count+1:]
                content = content.strip()
            else:
                content = item
        split_list.append((header_count,content))
    return split_list

#def count_headers(block):
    #split_block = block.split("\n")
    #split_list = []
    #header_count = 0
    #for item in split_block:
        #item = item.strip()
        #for i in range(len(item)):
            #if header_count == 6: 
                      #break
            #if item[i] == "#":
                #header_count += 1
            #else:
                 #break
        #split_list.append(header_count)
        #header_count = 0   
    #return split_list


def remove_leading_numbers_ol(block):
    split_block = block.split("\n")
    split_list = []
    for ln in split_block:
        ln = ln.strip()
        content = re.sub(r"^\d+\.\s*", "", ln)
        content = content.strip()
        split_list.append(content)
    return split_list

def remove_leading_ul(block):
    split_block = block.split("\n")
    split_list = []
    for ln in split_block:
        ln = ln.strip()
        content = ln[2:]
        content = content.strip()
        split_list.append(content)
    return split_list
    
def remove_leading_code_symbol(block):
    # assumes block starts/ends with ``` fences
    content = block[3:-3]
    if content.startswith("\n"):
        content = content[1:]
    # normalize trailing newlines to exactly one
    content = content.rstrip("\n") + "\n"
    return content

def remove_newline(block):
    one_line_block = block.replace("\n", " ")
    return one_line_block

def remove_leading_quote_symbol(block):
    no_quote_symbol_block = block.replace(">", "")
    return no_quote_symbol_block

def text_to_children(text):
    text_node_ls = text_to_textnodes(text)
    leaf_html_node_ls = []
    for tn in text_node_ls:
        leaf_node = text_node_to_html_node(tn)
        leaf_html_node_ls.append(leaf_node)
    return leaf_html_node_ls


    
