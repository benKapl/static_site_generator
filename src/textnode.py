from enum import Enum
from typing import Optional

from htmlnode import Tag, LeafNode

TextType = Enum("TextType", ["NORMAL", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None) -> None:
        self.text = text
        if not isinstance(text_type, TextType):
            raise Exception("not a valid text_type")
        self.text_type =  text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url):
            return True
        return False

    def __repr__(self):
        return f"Textnode(text={self.text}, text_type={self.text_type.__repr__()}, url={self.url})"


def text_node_to_html_node(text_node: TextNode):
    """
    Convert a TextNode to a LeafNode(HTMLNode)
    Return a LeafNode object
    """
    match text_node.text_type:
        case TextType.NORMAL:
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

    normal = TextNode("I am normal", TextType.NORMAL)
    bold = TextNode("I am bold", TextType.BOLD)
    italic = TextNode("I am bold", TextType.ITALIC)
    code = TextNode("I am some code line\nHello World", TextType.CODE)
    link = TextNode("I am a hyperlink, deal with it", TextType.LINK, "https://superlink.org")
    img = TextNode("image of something", TextType.IMAGE, "https://imglink.com")

    tests = [normal, bold, italic, code, link, img]


    # exception = TextNode("coucou", TextType.COUCOU)

    for test in tests: 
        print(test)
        leafnode = text_node_to_html_node(test) 
        print(leafnode.to_html())
