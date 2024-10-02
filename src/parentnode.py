from typing import Optional, List

from htmlnode import HTMLNode, Tag
from leafnode import LeafNode


class ParentNode(HTMLNode):
    """ParentNode class handle the nesting of HTML nodes inside of one another.
       Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    """

    def __init__(self, tag: Tag, children: List, props: Optional[dict] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Return the ParentNode and its children to a single concatenated HTML string
        """
        if not self.tag:
            raise ValueError("ParentNode object must have a tag")

        if not self.children:
            raise ValueError("ParentNode object must have children")

        return f"<{self.tag.value}>{''.join([child.to_html() for child in self.children])}</{self.tag.value}>"


if __name__ == "__main__":
    node_a = LeafNode(Tag.A, "I am a hyperlink", {"href": "https//myawesomelink.net", "target": "_blank"})
    node_p = ParentNode(Tag.P, [node_a])


    print(node_p.to_html())