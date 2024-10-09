import re
from typing import List

from htmlnode import Tag, HTMLNode, LeafNode, ParentNode
from splitinlines import split_nodes_delimiter, split_nodes_image, split_nodes_link
from splitblocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextType, TextNode


def text_to_textnodes(text: str) -> List[TextNode]:
    """Take a raw string full of inline markdown element and split it
    into a list of relevant TextNodes
    """
    if not text:
        return [TextNode("", TextType.TEXT)]
    firstnode = TextNode(f"{'' if not text else text}", TextType.TEXT)
    nodes_with_image = split_nodes_image([firstnode])
    nodes_with_link = split_nodes_link(nodes_with_image)
    nodes_with_bold = split_nodes_delimiter(nodes_with_link, "**", TextType.BOLD)
    nodes_with_italic = split_nodes_delimiter(nodes_with_bold, "*", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(nodes_with_italic, "`", TextType.CODE) # add code nodes
    
    # return all nodes with empty textnodes removed
    return [node for node in all_nodes if not (node.text=="" and TextType.TEXT)]
    return all_nodes


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
    document_nodes = []

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                document_nodes.append(ParentNode(tag=Tag.P, children=text_to_children(block)))
            case BlockType.HEADING:
                document_nodes.append(ParentNode(tag=get_heading_tag(block), 
                                                 children=text_to_children(format_markdown_heading(block))))
            case BlockType.CODE:
                document_nodes.append(ParentNode(tag=Tag.CODE, 
                                                 children=text_to_children(format_markdown_code(block))))
            case BlockType.QUOTE:
                document_nodes.append(ParentNode(tag=Tag.QUOTE, 
                                                 children=text_to_children(format_markdown_quote(block))))
            case BlockType.UNORDERED_LIST:
                document_nodes.append(ParentNode(Tag.UL, 
                                                 children=markdown_lists_to_li_nodes(text=block, index=2)))

            case BlockType.ORDERED_LIST:
                document_nodes.append(ParentNode(Tag.OL, 
                                                 children=markdown_lists_to_li_nodes(text=block, index=3)))
                
            case _:
                raise Exception("not a valid blocktype")

    return ParentNode(Tag.DIV, children=document_nodes)

# Helper functions for markdown_to_html_nodes below
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


def format_markdown_heading(text: str) -> str:
    """ Strip markdown hashtags at the beginning 
        of a markdown heading block
    """
    # get all hashtags
    markdown_headings = re.match(r'^#{1,6}', text).group() #type: ignore
    if not markdown_headings:
        raise Exception("not a valid heading block")
    return text.lstrip(markdown_headings).lstrip()


def format_markdown_code(text: str) -> str:
    """ Strip markdown code backticks at the beginning 
        and end of a markdown code block
    """
    lines = text.split("\n")
    if not "```" in (lines[0] and lines[-1]):
        raise Exception(("not a valid code block"))
    lines.pop(0)
    lines.pop()
    return "\n".join(lines).strip()


def format_markdown_quote(text: str) -> str:
    """ Strip markdown quote delimiter (">") and spaces
    at the begining of each code line
    """
    lines = text.split("\n")
    # removed block quotes from lines
    lines = [line.lstrip("> ") for line in lines]
    # Add html line break if there are more than one line
    if len(lines) > 1:
        return "\n".join([f"{line}<br>" for line in lines])
    return "\n".join(lines)


def markdown_lists_to_li_nodes(text: str, index: int) -> List[ParentNode]:
    """Takes a string block of markdown list elements (ordered and unordered),
    the index at which the line must be cut
    and return a list of ParentNode of tag LI with the formated lines
    """
    lines = text.split("\n")
    lines = [line[index:] for line in lines]
    return [ParentNode(Tag.LI, children=text_to_children(line)) for line in lines]
    


if __name__ == "__main__":
    from pprint import pprint
    input_text = "*entire text as italic*"


    ul_doc = """
> voici une preière list
> avec des élément **gras** mais non ordonnés

1. et de un
2. et de *deux*
3. et de trois
"""

    # pprint(markdown_to_html_node(ul_doc).children)
    # print(markdown_to_html_node(ul_doc).to_html())
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

>

etc ztc
"""

    print(markdown_to_html_node(big_doc).to_html())
