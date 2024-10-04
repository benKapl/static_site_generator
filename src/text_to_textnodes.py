import re
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

        elif delimiter not in node.text: # Old node is NORMAL
            new_nodes.append(node)   

        else:  # Old node has a delimiter
            parts = node.text.split(delimiter) 

            if len(parts) % 2 == 0:
                raise Exception(f"Unmatched delimiter '{delimiter}' found in text: '{node.text}'")
            
            # Transform part into textnode, alternate type between indexes
            # and add them to new_nodes
            for i in range(len(parts)):
                new_nodes.append(TextNode(parts[i], TextType.NORMAL if i % 2 == 0 else text_type))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # if there is no image, append the node as is
        if not extract_markdown_images(node.text):
            new_nodes.append(node)   

        else:
            text = node.text
            # retrieve the alt and url of each image in a list of tuples
            images = [image for image in extract_markdown_images(text)]

            for image in images:
                alt = image[0]
                url = image[1]
                # make a single into the node text on the image string
                parts = text.split(f"![{alt}]({url})", 1)
                # print(parts)

                # add a normal node of the first part and add a image node
                # with the retrive alt and url
                new_nodes.extend([TextNode(parts[0], TextType.NORMAL),
                                  TextNode(alt, TextType.IMAGE, url)])     
                
                # make the second half of the next part to be splitted 
                text = parts[-1]

                # add last text part if there is no image in it
                if not extract_markdown_images(text):
                    new_nodes.append(TextNode(parts[1], TextType.NORMAL))
                
    # return a list cleared of NORMAL nodes with empty text
    return [node for node in new_nodes if node.text or node.text_type == TextType.IMAGE]


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # if there is no image, append the node as is
        if not extract_markdown_links(node.text):
            new_nodes.append(node)   

        else:
            text = node.text
            # retrieve the alt and url of each image in a list of tuples
            links = [link for link in extract_markdown_links(text)]

            for image in links:
                anchor = image[0]
                url = image[1]
                # make a single into the node text on the image string
                parts = text.split(f"[{anchor}]({url})", 1)

                # add a normal node of the first part and add a link node
                # with the retrive alt and url
                new_nodes.extend([TextNode(parts[0], TextType.NORMAL),
                                  TextNode(anchor, TextType.LINK, url)])     
                
                # make the second half of the next part to be splitted 
                text = parts[-1]

                # add last text part if there is no image in it
                if not extract_markdown_links(text):
                    new_nodes.append(TextNode(parts[1], TextType.NORMAL))
                
    # return a list cleared of NORMAL nodes with empty text
    return [node for node in new_nodes if node.text or node.text_type == TextType.LINK]


def extract_markdown_images(text):
    """Takes a markdown string as input and return a tuple with :
    - alt text (index 0)
    - url (index 1)
    """
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
    """Takes a markdown string as input and return a tuple with :
    - alt text (index 0)
    - url (index 1)
    """
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)



if __name__ == "__main__":
    from pprint import pprint

    node = TextNode("![start](http://start.url) and ![middle](http://middle.url) then ![end](http://end.url) followed by text", TextType.NORMAL)
    result = split_nodes_image([node])
    pprint(result)

""" [
   TextNode("This is text with a ", TextType.NORMAL),
   TextNode("code block", TextType.CODE),r
   TextNode(" word", TextType.NORMAL),
]
"""

