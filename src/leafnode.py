from typing import Optional

from htmlnode import HTMLNode, Tag


class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
    """

    def __init__(self, tag: Tag | None, value: str, props: Optional[dict] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Return the LeafNode to a single concatenated HTML string
        """
        if not self.value:
            raise ValueError("LeafNode object must have a value")

        if not self.tag:
            return self.value  # An HTMLNode without a tag will just render as raw text

        return f"<{self.tag.value if not self.props else self.tag.value + ' ' + self.props_to_html()}>{self.value}</{self.tag.value}>"
