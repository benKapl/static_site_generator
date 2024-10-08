from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown: str) -> list:
    """Cut a document into blocks at each double line return
    Takes a raw Markdown string (representing a full document) as input 
    and returns a list of "block" strings.
    """
    blocks = markdown.split("\n\n")
    # Strip whitespace for each block
    stripped_blocks = [block.strip() for block in blocks]
    # Return a list with empty blocks removed
    return [block for block in stripped_blocks if block]


def block_to_block_type(block: str) -> BlockType:
    """Take a block of raw markdown text as input, and return its blocktype
    """
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else: 
        return BlockType.PARAGRAPH
        
def is_heading(text: str) -> bool:
    """Determine if the input text is a markdown heading"""
    pattern = r'^#{1,6} .*$'
    return bool(re.match(pattern, text))

def is_code(text: str) -> bool:
    """Determine if the input text is a markdown code block"""
    pattern = r'^```.*```$'
    return bool(re.match(pattern, text))

def is_quote(text: str) -> bool:
    """Determine if the input text is a markdown quote block"""
    pattern = r'^>.*$'
    # All lines start with ">"
    return all(re.match(pattern, line) for line in text.split('\n'))

def is_unordered_list(text: str) -> bool:
    """Determine if the input text is a markdown unordered list block"""
    pattern = r'^[*-] .*$'
    # All lines start with "*" or "-" followed by a space
    return all(re.match(pattern, line) for line in text.split('\n'))

def is_ordered_list(text: str) -> bool:
    """Determine if the input text is a markdown ordered list block"""
    lines = text.split('\n')
    # Start with a number in ascending order followed by a point and space
    pattern = [f"{i}. " for i in range(1, len(lines) + 1)]
    # Compare pattern with a list of the first 3 characters of each line
    numbers = [line[0:3] for line in lines]
    return numbers == pattern


if __name__ == "__main__":
    from pprint import pprint

    test = "1. dsfzf\n2.       sdfsdfs\n4. sdfsdfs"

    print(is_ordered_list(test))
    # print(block_to_block_type(test))


    # pprint(markdown_to_blocks(test))
    # print(len(markdown_to_blocks(test)))


