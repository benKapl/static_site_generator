from typing import List

from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """Takes a list of "old nodes", a delimiter, and a text type. 
    Returns a new list of nodes, where any "text" type nodes in the input list are (potentially) 
    split into multiple nodes based on the syntax. 
    """
    new_nodes = []
    for node in old_nodes:
        
        # If an "old node" is not a "text" type, just add it to the new list as-is
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)

        else:        
            if node.text_type == TextType.NORMAL and delimiter not in node.text:
                raise Exception(f"Delimiter '{delimiter}' is not a valid Markdown syntax")
            
            splitted_text = node.text.split(delimiter)

            if len(splitted_text) % 2 == 0:
                raise Exception("Imbalanced delimiter situation")

            def nodes_to_extend(even_text_type, odd_text_type):
                """ Creates the new nodes and add them in a list based on the index of the text they are based on.
                Take two arguments : 
                - text-type for even index
                - text-type for odd_index
                Return a list with the nodes in the right ordre
                """
                nodes_to_add = []
                for i in range(len(splitted_text)):
                    nodes_to_add.append(TextNode(splitted_text[i], text_type=even_text_type if i % 2 == 0 else odd_text_type))
                return nodes_to_add

            # Check if the element at index 0 is not empty -> the text doesn't start with the delimiter
            if splitted_text[0]:
                new_nodes.extend(nodes_to_extend(even_text_type=TextType.NORMAL, odd_text_type=text_type))
            else:
                splitted_text = splitted_text[1:-1] #strip the empty element at the edges of the list
                new_nodes.extend(nodes_to_extend(even_text_type=text_type, odd_text_type=TextType.NORMAL))

    return new_nodes



    # Simple function with split() and extend(). not need for function transformation.
    # We assume the delimiter is know in advance, the logic of chosing the text_type based on the 
    # delimiter is done elsewhere.

if __name__ == "__main__":
    from pprint import pprint

    node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    node2 = TextNode("**This is a bold text** with a **bold content**", TextType.NORMAL)

    code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    bold_nodes = split_nodes_delimiter([node2], "**", TextType.BOLD)

    new_nodes = code_nodes

    for node in new_nodes:
        htmlnode = text_node_to_html_node(node)
        print(htmlnode.to_html())

    pprint(new_nodes)


""" [
   TextNode("This is text with a ", TextType.NORMAL),
   TextNode("code block", TextType.CODE),
   TextNode(" word", TextType.NORMAL),
]
"""

