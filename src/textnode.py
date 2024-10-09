from enum import Enum
from typing import Optional

from htmlnode import Tag, LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


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


if __name__ == "__main__":
    pass


