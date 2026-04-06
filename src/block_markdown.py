from enum import Enum
import re

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



