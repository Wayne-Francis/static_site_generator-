
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks_list = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            blocks_list.append(stripped_block)
    return blocks_list

    