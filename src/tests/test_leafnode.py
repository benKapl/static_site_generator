from unittest import main, TestCase

from htmlnode import Tag
from leafnode import LeafNode


class TestLeafNode(TestCase):
    def test_init_without_value(self):
        with self.assertRaises(TypeError):
            LeafNode(tag=None)  # type: ignore

    def test_init_without_tag(self):
        with self.assertRaises(TypeError):
            LeafNode(value="value")  # type: ignore

    def test_value_is_none(self):
        node = LeafNode(tag=Tag.P, value=None)  # type: ignore
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