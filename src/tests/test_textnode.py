from unittest import main, TestCase

from textnode import TextNode, TextType


class TestTextNode(TestCase):
    def test_equal_with_all_properties(self):
        node1 = TextNode("This is a text", TextType.BOLD, "https://www.url.com")
        node2 = TextNode("This is a text", TextType.BOLD, "https://www.url.com")
        self.assertEqual(node1, node2)

    def test_equal_with_no_url(self):
        node1 = TextNode("This is a new text", TextType.NORMAL)
        node2 = TextNode("This is a new text", TextType.NORMAL)
        self.assertEqual(node1, node2)

    def test_not_eq_with_diff_text(self):
        node1 = TextNode("This is a text", TextType.NORMAL)
        node2 = TextNode("This is a different text", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_not_eq_with_diff_texttype(self):
        node1 = TextNode("This is a text", TextType.NORMAL)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_with_diff_url(self):
        node1 = TextNode("This is a text", TextType.NORMAL, "https://www.url.com")
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_testtype_isnot_TextType_object(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a text", "normal") # type: ignore

    def test_testtype_isnot_valid_TextType_value(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is a text", TextType.normal) # type: ignore

if __name__ == '__main__':
    main()