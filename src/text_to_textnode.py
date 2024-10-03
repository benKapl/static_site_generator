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

        else:  # Old node is NORMAL
            if delimiter not in node.text:
                new_nodes.append(node)   

            else:  # Old node has a delimiter
                parts = node.text.split(delimiter)

                if len(parts) % 2 == 0:
                    raise Exception(f"Unmatched delimiter '{delimiter}' found in text: '{node.text}'")
                
                # Transform part into textnode, alternate type between indexes
                nodes_to_add = []
                for i in range(len(parts)):
                    nodes_to_add.append(TextNode(parts[i], TextType.NORMAL if i % 2 == 0 else text_type))
                
                # add all notes to the new_nodes list
                new_nodes.extend(nodes_to_add)

    return new_nodes



    # Simple function with split() and extend(). not need for function transformation.
    # We assume the delimiter is know in advance, the logic of chosing the text_type based on the 
    # delimiter is done elsewhere.

if __name__ == "__main__":
    from pprint import pprint

    node = TextNode("*Italic* is who i am", TextType.NORMAL)
    result = split_nodes_delimiter([node], "*", TextType.ITALIC)
    
    pprint(result)

""" [
   TextNode("This is text with a ", TextType.NORMAL),
   TextNode("code block", TextType.CODE),
   TextNode(" word", TextType.NORMAL),
]
"""

