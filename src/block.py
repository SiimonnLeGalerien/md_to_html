from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if len(re.findall(r"^\#{1,6}\ .+$", block)) == 1:
        return BlockType.HEADING
    if len(re.findall(r"^```\w*\n([\s\S]*?)```$", block)) == 1:
        return BlockType.CODE
    block_split = block.split("\n")
    is_quote = True
    for quote in block_split:
        if not quote.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    is_unordered = True
    for unordered_list in block_split:
        if len(re.findall(r"^\- .+$", unordered_list)) != 1:
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for ordered_list in block_split:
        if len(re.findall(r"^\d+\.\ .+$", ordered_list)) != 1:
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

