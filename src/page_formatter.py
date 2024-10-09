import re
from typing import List

from htmlnode import Tag, HTMLNode, LeafNode, ParentNode
from splitinlines import split_nodes_delimiter, split_nodes_image, split_nodes_link
from splitblocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextType, TextNode


def is_markdown_image(text: str) -> bool:
    """Determine if the input text is a markdown image"""
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return bool(re.match(pattern, text))


def is_markdown_link(text: str) -> bool:
    """Determine if the input text is a markdown link"""
    pattern = r'\[(.*?)\]\((.*?)\)'
    return bool(re.match(pattern, text))


def text_to_textnodes(text: str) -> List[TextNode]:
    """Take a raw string full of inline markdown element and split it
    into a list of relevant TextNodes
    """
    firstnode = TextNode(text, TextType.TEXT)
    nodes_with_image = split_nodes_image([firstnode])
    nodes_with_link = split_nodes_link(nodes_with_image)
    nodes_with_bold = split_nodes_delimiter(nodes_with_link, "**", TextType.BOLD)
    nodes_with_italic = split_nodes_delimiter(nodes_with_bold, "*", TextType.ITALIC)
    nodes_with_code = split_nodes_delimiter(nodes_with_italic, "`", TextType.CODE)
    
    # return all nodes with empty textnodes removed
    return [node for node in nodes_with_code if not (node.text=="" and TextType.TEXT)]


def text_node_to_html_node(text_node: TextNode):
    """
    Convert a TextNode to a LeafNode(HTMLNode)
    Return a LeafNode object
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode(Tag.B, value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(Tag.I, value=text_node.text)

        case TextType.CODE:
            return LeafNode(Tag.CODE, value=text_node.text)
        
        case TextType.LINK:
            return LeafNode(Tag.A, value=text_node.text, props={"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode(Tag.IMG, value="", props={"src": text_node.url, "alt": text_node.text})

        # case _:
        #     raise Exception("not a valid text_type")


def text_to_children(text: str) -> List[HTMLNode]:
    """Takes a raw text and return a list of HTMLNodes
    """
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]


def markdown_to_html_node(markdown: str) -> HTMLNode:

    blocks = markdown_to_blocks(markdown)
    for block in blocks: 
        print(block)
    document_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                document_nodes.append(ParentNode(tag=Tag.P, children=text_to_children(block)))
            case BlockType.HEADING:
                document_nodes.append(ParentNode(tag=get_heading_tag(block), 
                                                 children=text_to_children(strip_markdown_heading(block))))
            case BlockType.CODE:
                document_nodes.append(ParentNode(tag=Tag.CODE, 
                                                 children=text_to_children(strip_markdown_code(block))))

    return ParentNode(Tag.DIV, children=document_nodes)
## ATTENTION : Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.


def get_heading_tag(text: str) -> Tag:
    """ Return the html heading tag of a markdown text block 
    based on the number of hashtags in it
    """
    # Get the number of "#" in the beginning of the block
    heading_type = len(re.match(r'^#{1,6}', text).group()) #type: ignore
    
    match heading_type:
        case 1:
            return Tag.H1
        case 2:
            return Tag.H2
        case 3:
            return Tag.H3
        case 4:
            return Tag.H4
        case 5:
            return Tag.H5
        case 6:
            return Tag.H6
        case _:
            raise Exception("invalid number of #")


def strip_markdown_heading(text: str) -> str:
    """ Strip markdown hashtags at the beginning 
        of a markdown heading block
    """
    # get all hashtags
    markdown_headings = re.match(r'^#{1,6}', text).group() #type: ignore
    if not markdown_headings:
        raise Exception("not a valid heading block")
    return text.lstrip(markdown_headings).lstrip()


def strip_markdown_code(text: str) -> str:
    """ Strip markdown code backticks at the beginning 
        and end of a markdown code block
    """
    lines = text.split("\n")
    if not "```" in (lines[0] and lines[-1]):
        raise Exception(("not a valid code block"))
    lines.pop(0)
    lines.pop()
    return "\n".join(lines).strip()




if __name__ == "__main__":
    from pprint import pprint

    text = "This is a **bold text** with an *italic* word and a `code block` and **another bold text** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    # pprint(nodes)

    children = [text_node_to_html_node(node) for node in nodes]
    node1 = ParentNode(tag=Tag.P, children=children)
    node2 = LeafNode(None, value="some more text")    
    master_parent = ParentNode(Tag.DIV, children=[node1, node2])
    # print(master_parent.to_html())
    # pprint(html_elements)
    # print("".join([leafnode.to_html() for leafnode in html_elements]))


    html_doc = """
## Partie 1

Voici une partie avec un headings. Je vais mettre un image tient : ![Big O Graph](https://cdn-media-1.freecodecamp.org/images/1*KfZYFUT2OKfjekJlCeYvuQ.jpeg)

Ainsi qu'un lien : [-- source](https://www.bigocheatsheet.com/)

```python
def add(a, b)
    return a + b
```

## partie 2

coucou la partie 2 !
"""

    # pprint(markdown_to_html_node(html_doc).children)
    print(markdown_to_html_node(html_doc).to_html())
    # for i in markdown_to_blocks(html_doc):
    #     print(i)



    big_doc = """
["Big O"](https://en.wikipedia.org/wiki/Big_O_notation) analysis (pronounced "Big Oh", not "Big Zero") is one way to compare the practicality of algorithms.

>[!hint] Big O is a characterization of algorithms according to their worst-case growth rates

We write Big-O notation like this: `O(formula)`

Where `formula` describes how an algorithm's run time or space requirements grow **as the input size grows.**

- [[O(1)]] - constant
- [[O(log(n))]] - logarithmic
- [[O(n)]] - linear
- [[O(n x log(n))]]
- [[O(n^2)]] - squared   + a peculiar one : [[O(nm)]]
- [[O(2^n)]] - exponential
- [[O(n!)]] - factorial

The following chart shows the growth rate of several different Big O categories. The size of the input is shown on the `x axis` and how long the algorithm will take to complete is shown on the `y axis`.

![Big O Graph](https://cdn-media-1.freecodecamp.org/images/1*KfZYFUT2OKfjekJlCeYvuQ.jpeg)

[-- source](https://www.bigocheatsheet.com/)

As the size of inputs grows, the algorithms become slower to complete (take longer to run). The _rate_ at which they become slower is defined by their Big O category.

For example, `O(n)` algorithms slow down more slowly than `O(n^2)` algorithms.

## The worst Big-O category?

The algorithms that slow down the fastest in our chart are the factorial and exponential algorithms, or `O(n!),` and `O(2^n)`.


> [!attention] [[Constants don't matter]]

"""