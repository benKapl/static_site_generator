from enum import Enum
from dataclasses import dataclass
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

@dataclass
class HTMLNode:
    tag: Optional[Tag] = None
    value: Optional[str] = None
    children: Optional[List] = None
    props: Optional[dict] = None
    
    # force type checking
    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
            
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        """ Transform the attributes in the props dictionnary into a html readble attribute
        """
        prop_string =""
        for key, value in self.props.items(): # type: ignore
            prop_string += f'{key}="{value}" '

        return prop_string.strip()
    
if __name__ == "__main__":

    foo = HTMLNode(tag=Tag.A, 
                   props={"href": "https://www.google.com", "target": "_blank"})
    
    bar = HTMLNode()

    node = HTMLNode(Tag.P, "This is a paragraph", [bar], {"class": "my_class"}) 

    print(node)