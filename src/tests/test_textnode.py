from unittest import main, TestCase

from textnode import TextNode, TextType, text_node_to_html_node


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

# Continue with pytest
class TestTextNodeToHtml:
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






if __name__ == '__main__':
    main()