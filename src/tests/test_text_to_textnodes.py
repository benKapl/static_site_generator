import pytest

from textnode import TextNode, TextType
from text_to_textnodes import (split_nodes_delimiter, 
                               split_nodes_image,
                               split_nodes_link,
                               extract_markdown_images, 
                               extract_markdown_links)

class TestSplitNodesDelimiter:
    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert result == [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text",TextType.NORMAL)
        ]

    def test_text_starts_with_italic_part(self):
        node = TextNode("*Italic* is who i am ", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert result == [
            TextNode("", TextType.NORMAL),
            TextNode("Italic", TextType.ITALIC),
            TextNode(" is who i am ", TextType.NORMAL),
        ]   

    def test_multiple_code_delimiters(self):
        node = TextNode("Here's some `inline code` and more `code`", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            TextNode("Here's some ", TextType.NORMAL),
            TextNode("inline code", TextType.CODE),
            TextNode(" and more ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.NORMAL)
        ]

    def test_append_nodes_with_not_NORMAL_TextType(self):
        code_node = TextNode("`I am a code line`", TextType.CODE)
        italic_node = TextNode("`I am an italic line`", TextType.ITALIC)
        result = split_nodes_delimiter([code_node, italic_node], "", TextType.NORMAL)
        assert result == [
            TextNode("`I am a code line`", TextType.CODE),
            TextNode("`I am an italic line`", TextType.ITALIC)
        ]

    def test_imbalanced_delimiter(self):
        with pytest.raises(Exception):
            node = TextNode("`code block` text with non closed `delimiter", TextType.NORMAL)
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestSplitNodesImages:
    def test_single_image(self):
        node = TextNode("Check out this ![alt](http://image.url)", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Check out this ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "http://image.url")
        ]
        assert result == expected
    
    def test_multiple_images(self):
        node = TextNode("Image one ![one](http://one.url) and two ![two](http://two.url)", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("Image one ", TextType.NORMAL),
            TextNode("one", TextType.IMAGE, "http://one.url"),
            TextNode(" and two ", TextType.NORMAL),
            TextNode("two", TextType.IMAGE, "http://two.url")
        ]
        assert result == expected
    
    def test_no_image(self):
        node = TextNode("Just text with no image", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [node]
        assert result == expected
    
    def test_starts_with_image(self):
        node = TextNode("![start](http://start.url) followed by text", TextType.NORMAL)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "http://start.url"),
            TextNode(" followed by text", TextType.NORMAL)
        ]
        assert result == expected


class TestSplitNodesLinks:
    def test_single_link(self):
        node = TextNode("Visit [Boot.dev](http://boot.dev)", TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.NORMAL),
            TextNode("Boot.dev", TextType.LINK, "http://boot.dev")
        ]
        assert result == expected

    def test_multiple_links(self):
        node = TextNode("Here's a [link](http://link1.com) and another [link](http://link2.com).", TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("Here's a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://link1.com"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://link2.com"),
            TextNode(".", TextType.NORMAL),
        ]
        assert result == expected

    def test_no_link(self):
        node = TextNode("Plain text without links", TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [node]
        assert result == expected

    def test_starts_with_link(self):
        node = TextNode("[Boot.dev](http://boot.dev) is a great site", TextType.NORMAL)
        result = split_nodes_link([node])
        expected = [
            TextNode("Boot.dev", TextType.LINK, "http://boot.dev"),
            TextNode(" is a great site", TextType.NORMAL)
        ]
        assert result == expected


class TestExtractMdImages:
    def test_single_image(self):
        text = "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        assert extract_markdown_images(text) == [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

    def test_multiple_images(self):
        text = "This is text with images ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        assert extract_markdown_images(text) == [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    def test_no_images(self):
        text = "This is text with no images"
        assert extract_markdown_images(text) == []

    def test_empty_string(self):
        text = ""
        assert extract_markdown_images(text) == []

    def test_special_characters(self):
        text = "This is text with an image ![[rick@roll)](https://i.imgur.com/aKaOqIh.gif)"
        assert extract_markdown_images(text) == [("[rick@roll)", "https://i.imgur.com/aKaOqIh.gif")]


class TestExtractMdLinks:
    def test_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        assert extract_markdown_links(text) == [("to boot dev", "https://www.boot.dev")]

    def test_multiple_links(self):
        text = "This is text with links [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        assert extract_markdown_links(text) == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    def test_no_links(self):
        text = "This is text with no links"
        assert extract_markdown_links(text) == []

    def test_empty_string(self):
        text = ""
        assert extract_markdown_links(text) == []

    def test_special_characters(self):
        text = "This is text with a link [t(o@boot dev]]](htttps://www.boo}t.dev)"
        assert extract_markdown_links(text) == [("t(o@boot dev]]", "htttps://www.boo}t.dev")]
