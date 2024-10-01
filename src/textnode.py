from typing import Optional


class  TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None) -> None:
        self.text = text
        self.text_type =  text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"Textnode({self.text}, {self.text_type}, {self.url})"
        

if __name__ == "__main__":

    foo = TextNode("foo", "norma")
    bar = TextNode("foo", "normal")

    print(foo == bar)
    print(bar)
