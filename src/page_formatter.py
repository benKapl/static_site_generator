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
    # If the number is aobe
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
    return text.lstrip(markdown_headings).lstrip()


def format_markdown_code(text: str) -> str:
    """ Strip markdown code backticks at the beginning 
        and end of a markdown code block
    """
    lines = text.split("\n")
    if not re.match(r'^```', lines[0]) or not re.search(r'```$', lines[-1]):
        raise Exception(("not a valid code block"))
    lines.pop(0)
    lines.pop()
    return "\n".join(lines).strip()


def format_markdown_quote(text: str) -> str:
    """ Strip markdown quote delimiter (">") and spaces
    at the begining of each code line
    """
    lines = text.split("\n")
    # Remove block quotes from lines
    # and add html line break if there are more than one line
    return "<br>".join([line.lstrip("> ") for line in lines])


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
    text = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```"""

    print(markdown_to_html_node(text).to_html())
