import sys
from unittest import main, TestCase

from htmlnode import Tag, HTMLNode, LeafNode


class TestHTMLNode(TestCase):
    def test_default_properties(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_all_properties(self):
        children_node = HTMLNode()
        node = HTMLNode(Tag.P, "This is a paragraph", [children_node], {"class": "my_class"}) 
        self.assertEqual(node.tag, Tag.P)
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.children, [children_node])
        self.assertEqual(node.props, {"class": "my_class"})

    def test_tag_isnot_Tag_object(self):
        with self.assertRaises(Exception):
            HTMLNode(tag="p") # type: ignore

    def test_props_to_html(self):
        node = HTMLNode(tag=Tag.A, 
                   props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')


class TestLeafNode(TestCase):
    def test_init_without_value(self):
        with self.assertRaises(TypeError):
            LeafNode(tag=None) # type: ignore

    def test_init_without_tag(self):
        with self.assertRaises(TypeError):
            LeafNode(value="value") # type: ignore

    def test_value_is_none(self):
        node = LeafNode(tag=Tag.P, value=None) # type: ignore
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tag_is_none(self):
        node = LeafNode(tag=None, value="This is a raw text")
        self.assertEqual(node.to_html(), "This is a raw text")     

    def test_tag_without_props(self):
        node = LeafNode(value="This is a paragraph", tag=Tag.P)
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")     

    def test_tag_with_props(self):
        node = LeafNode(value="This is a link", tag=Tag.A, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">This is a link</a>')


        
if __name__ == '__main__':
    main()