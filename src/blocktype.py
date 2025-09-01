
from enum import Enum
from markdown_to_blocks import markdown_to_blocks

class BlockType(Enum):
   paragraph = "paragraph"
   heading = "heading"
   code = "code"
   quote = "quote"
   unordered_list = "unordered_list"
   ordered_list = "ordered_list"

def block_to_block_type(markdown):
    #blocks = markdown_to_blocks(markdown)
    if markdown.startswith("'''") and markdown.endswith("'''"):
            return BlockType.code
    header_count = 0
    for i in range(len(markdown)):
            if header_count == 6: 
                      break
            if markdown[i] == "#":
                header_count += 1
            else:
                 break
    if header_count < len(markdown):
        if header_count > 0 and markdown[header_count] == " ":
            return BlockType.heading
    markdown_lines = markdown.split("\n")
    all_lines_are_quotes = True
    all_lines_are_Unordered_lists = True
    all_lines_are_ordered_lists = True
    number_order = 1
    for lines in markdown_lines:
        try:    
            dot_index = lines.find(".")
            if dot_index <= 0:
                all_lines_are_ordered_lists = False
                break
            if dot_index + 1 >= len(lines) or lines[dot_index + 1] != " ":
                all_lines_are_ordered_lists = False
                break
            line_number = int(lines[:dot_index])
            if line_number != number_order:
                all_lines_are_ordered_lists = False
                break
            number_order += 1
        except ValueError: # Catches errors if int() conversion fails
            all_lines_are_ordered_lists = False
            break
        except IndexError: # Catches errors if lines[dot_index + 1] is out of bounds due to unexpected short strings
            all_lines_are_ordered_lists = False
            break
    for lines in markdown_lines:
        if not lines.startswith(">"):
            all_lines_are_quotes = False
            break
    for lines in markdown_lines:
        if not lines.startswith("- "):
            all_lines_are_Unordered_lists = False
            break
    if all_lines_are_ordered_lists:
        return BlockType.ordered_list
    elif all_lines_are_Unordered_lists:
        return BlockType.unordered_list
    elif all_lines_are_quotes:
        return BlockType.quote
    else:
         return BlockType.paragraph
    
        