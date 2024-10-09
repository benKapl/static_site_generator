from unittest import main, TestCase

from textnode import TextNode, TextType
from page_formatter import text_node_to_html_node


class TestTextNode(TestCase):
    def test_equal_with_all_properties(self):
        node1 = TextNode("This is a text", TextType.BOLD, "https://www.url.com")
        node2 = TextNode("This is a text", TextType.BOLD, "https://www.url.com")
        self.assertEqual(node1, node2)

    def test_equal_with_no_url(self):
        node1 = TextNode("This is a new text", TextType.TEXT)
        node2 = TextNode("This is a new text", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_not_eq_with_diff_text(self):
        node1 = TextNode("This is a text", TextType.TEXT)
        node2 = TextNode("This is a different text", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_with_diff_texttype(self):
        node1 = TextNode("This is a text", TextType.TEXT)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_with_diff_url(self):
        node1 = TextNode("This is a text", TextType.TEXT, "https://www.url.com")
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_test_type_isnot_TextType_object(self):
        with self.assertRaises(Exception):
            TextNode("This is a text", "normal") # type: ignore

    def test_test_type_isnot_valid_TextType_value(self):
        with self.assertRaises(AttributeError):
            TextNode("This is a text", TextType.normal) # type: ignore


if __name__ == '__main__':
    main()