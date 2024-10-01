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
        """ Transform the attributes in the props dictionnary into a html readble attribute
        """
        prop_string =""
        for key, value in self.props.items(): # type: ignore
            prop_string += f'{key}="{value}" '

        return prop_string.strip()
    
class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
    """
    pass
    # super().__init___()

if __name__ == "__main__":

    foo = HTMLNode()
    
    # bar = HTMLNode()

    # node = HTMLNode(Tag.P, "This is a paragraph", [bar], {"class": "my_class"}) 

    print(foo)