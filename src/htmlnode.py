from enum import Enum
from typing import Optional, List, Dict


class Tag(Enum):
    P = "p"
    A = "a"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    IMG = "img"


class HTMLNode:
    def __init__(self, tag: Optional[Tag] = None, value: Optional[str] = None, 
                       children: Optional[List] = None, props: Optional[dict] = None):
        if tag != None and not isinstance(tag, Tag):
            raise Exception("not a valid tag")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag={self.tag.__repr__()}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        """ Transform the attributes in the props dictionnary into a html readable attribute
        """
        prop_string =""
        for key, value in self.props.items(): # type: ignore
            prop_string += f'{key}="{value}" '

        return prop_string.strip()
    
    
class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
    """
    def __init__(self, value: str, tag: Optional[Tag] = None, props: Optional[dict] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have a value")
        
        if not self.tag:
            return self.value # An HTMLNode without a tag will just render as raw text
        
        # return f"<{self.tag.value} {self.props_to_html() if self.props else ''}>{self.value}</{self.tag.value}>"
        return f"<{self.tag.value if not self.props else self.tag.value + ' ' + self.props_to_html()}>{self.value}</{self.tag.value}>"
        


        

if __name__ == "__main__":

    node2 = LeafNode(value="This is a paragraph", tag=Tag.P)
    node3 = LeafNode("This is a raw text")


