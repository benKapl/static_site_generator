import re
from typing import List

from textnode import TextNode, TextType, text_node_to_html_node


def extract_markdown_images(text: str) -> list:
    """Takes a markdown string as input and return a tuple with :
    - alt text (index 0)
    - url (index 1)
    """
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text: str) -> list:
    """Takes a markdown string as input and return a tuple with :
    - alt text (index 0)
    - url (index 1)
    """
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """Takes a list of "old nodes", a delimiter, and a text type. 
    Returns a new list of nodes, where any "text" type nodes in the input list are (potentially) 
    split into multiple nodes based on the syntax. 
    """
    new_nodes = []
    for node in old_nodes:
        
        # If an "old node" is not a "text" type, just add it to the new list as-is
        if node.text_type != TextType.TEXT:
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
                new_nodes.append(TextNode(parts[i], TextType.TEXT if i % 2 == 0 else text_type))

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
                new_nodes.extend([TextNode(parts[0], TextType.TEXT),
                                  TextNode(alt, TextType.IMAGE, url)])     
                
                # make the second half of the next part to be splitted 
                text = parts[-1]

                # add last text part if there is no image in it
                if not extract_markdown_images(text):
                    new_nodes.append(TextNode(parts[1], TextType.TEXT))
                
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
                new_nodes.extend([TextNode(parts[0], TextType.TEXT),
                                  TextNode(anchor, TextType.LINK, url)])     
                
                # make the second half of the next part to be splitted 
                text = parts[-1]

                # add last text part if there is no image in it
                if not extract_markdown_links(text):
                    new_nodes.append(TextNode(parts[1], TextType.TEXT))
                
    # return a list cleared of NORMAL nodes with empty text
    return [node for node in new_nodes if node.text or node.text_type == TextType.LINK]


def text_to_textnodes(text):
    textnode_only = TextNode(text, TextType.TEXT)
    text_bold = split_nodes_delimiter([textnode_only], "**", TextType.BOLD)
    text_bold_italic = split_nodes_delimiter(text_bold, "*", TextType.ITALIC)
    text_bold_italic_code = split_nodes_delimiter(text_bold_italic, "`", TextType.CODE)
    text_bold_italic_code_img = split_nodes_image(text_bold_italic_code)
    text_bold_italic_code_img_link = split_nodes_link(text_bold_italic_code_img)


    return text_bold_italic_code_img_link




if __name__ == "__main__":
    from pprint import pprint

    text = "This is a **bold text** with an *italic* word and a `code block` and **another bold text** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    textnode = TextNode("This is an image ", TextType.TEXT)
    nodes = text_to_textnodes(textnode)
    print(nodes)

    html_elements = [text_node_to_html_node(node) for node in nodes]
    print("".join([leafnode.to_html() for leafnode in html_elements]))
    # for node in nodes: 
    #         print(node)
    #         leafnode = text_node_to_html_node(node) 
    #         print(leafnode.to_html())


""" [
   TextNode("This is text with a ", TextType.NORMAL),
   TextNode("code block", TextType.CODE),r
   TextNode(" word", TextType.NORMAL),
]
"""

