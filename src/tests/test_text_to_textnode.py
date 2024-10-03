import pytest

from textnode import TextNode, TextType
from text_to_textnode import split_nodes_delimiter

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
