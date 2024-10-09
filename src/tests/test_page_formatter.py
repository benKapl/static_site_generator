from page_formatter import (text_to_textnodes, 
                            text_node_to_html_node,
                            markdown_to_html_node)
 
from textnode import TextType, TextNode


class TestTextToTextNodes:

    def test_all_cases(self):
        input_text = """This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        assert text_to_textnodes(input_text) == expected_output

    def test_several_bold_delimiters(self):
        input_text = "This is **bold text** and **another bold** section."
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" section.", TextType.TEXT)
]
        assert text_to_textnodes(input_text) == expected_output

    def test_entire_text_italic(self):
        input_text = "*entire text as italic*"
        assert text_to_textnodes(input_text) == [TextNode("entire text as italic", TextType.ITALIC)]

    def test_multiple_images(self):
        input_text = "This is an image ![first image](http://example.com/1.jpg) and another image ![second image](http://example.com/2.jpg)."
        expected_output = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("first image", TextType.IMAGE, "http://example.com/1.jpg"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "http://example.com/2.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        assert text_to_textnodes(input_text) == expected_output

    def test_entire_text_link(self):
        input_text = "[Boot.dev](https://boot.dev)"
        assert text_to_textnodes(input_text) == [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")]

    def test_input_is_textnode(self):
        pass


class TestTextNodeToHtmlNode:
    def test_text_node_to_html_node_normal(self):
        text_node = TextNode("I am normal", TextType.TEXT)
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == "I am normal"

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("I am bold", TextType.BOLD)
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == "<b>I am bold</b>"

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("I am italic", TextType.ITALIC)
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == "<i>I am italic</i>"
        
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("I am some code line\nHello World", TextType.CODE)
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == "<code>I am some code line\nHello World</code>"

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("I am a hyperlink, deal with it", TextType.LINK, "https://superlink.org")
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == '<a href="https://superlink.org">I am a hyperlink, deal with it</a>'

    def test_text_node_to_html_node_img(self):
        text_node = TextNode("image of something", TextType.IMAGE, "https://imglink.com")
        transformed_node = text_node_to_html_node(text_node)
        assert transformed_node.to_html() == '<img src="https://imglink.com" alt="image of something"></img>'
        
        # bold = TextNode("I am bold", TextType.BOLD)
        # italic = TextNode("I am bold", TextType.ITALIC)
        # code = TextNode("I am some code line\nHello World", TextType.CODE)
        # link = TextNode("I am a hyperlink, deal with it", TextType.LINK, "https://superlink.org")
        # img = TextNode("image of something", TextType.IMAGE, "https://imglink.com")




