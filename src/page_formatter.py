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
    if is_markdown_image(text):
        firstnode = TextNode(text, TextType.IMAGE)
    elif is_markdown_link(text): 
        firstnode = TextNode(text, TextType.LINK)
    else:
        firstnode = TextNode(text, TextType.TEXT)
        
    nodes_with_bold = split_nodes_delimiter([firstnode], "**", TextType.BOLD)
    nodes_with_italic = split_nodes_delimiter(nodes_with_bold, "*", TextType.ITALIC)
    nodes_with_code = split_nodes_delimiter(nodes_with_italic, "`", TextType.CODE)
    nodes_with_image = split_nodes_image(nodes_with_code)
    nodes_with_link = split_nodes_link(nodes_with_image)

    return nodes_with_link


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


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    document_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                textnodes = text_to_textnodes(block)
                children = [text_node_to_html_node(node) for node in textnodes]
                parent_node = ParentNode(tag=Tag.P, children=children)
                document_nodes.append(parent_node)
            case BlockType.HEADING:
                pass

    return ParentNode(Tag.DIV, children=document_nodes)



## ATTENTION : Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.






if __name__ == "__main__":
    text = "[Big O Graph](htthjkjps://cdn-media-1.freecodecamp.org/images/1*KfZYFUT2OKfjekJlCeYvuQ.jpeg)"
    print(is_markdown_link(text))


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

    pprint(markdown_to_html_node(html_doc))
    # for i in markdown_to_blocks(html_doc):
    #     print(i)
