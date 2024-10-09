from typing import List

from htmlnode import LeafNode, Tag
from splitinlines import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextType, TextNode


def markdown_to_html_node(markdown):
    pass



## ATTENTION : Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.


def text_to_textnodes(text: str) -> List[TextNode]:
    """Take a raw string full of inline markdown element and split it
    into a list of relevant TextNodes
    """
    textnode_only = TextNode(text, TextType.TEXT)
    text_bold = split_nodes_delimiter([textnode_only], "**", TextType.BOLD)
    text_bold_italic = split_nodes_delimiter(text_bold, "*", TextType.ITALIC)
    text_bold_italic_code = split_nodes_delimiter(text_bold_italic, "`", TextType.CODE)
    text_bold_italic_code_image = split_nodes_image(text_bold_italic_code)
    text_bold_italic_code_image_link = split_nodes_link(text_bold_italic_code_image)

    return text_bold_italic_code_image_link


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


if __name__ == "__main__":
    from pprint import pprint

    text = "This is a **bold text** with an *italic* word and a `code block` and **another bold text** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)

    html_elements = [text_node_to_html_node(node) for node in nodes]
    # pprint(html_elements)
    print("".join([leafnode.to_html() for leafnode in html_elements]))
