from unittest import main, TestCase

from htmlnode import Tag, HTMLNode


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

        
if __name__ == '__main__':
    main()