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



if __name__ == "__main__":
    from pprint import pprint

    test = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item
"""


    pprint(markdown_to_blocks(test))
    # print(len(markdown_to_blocks(test)))


