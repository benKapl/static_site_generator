from unittest import main, TestCase

from htmlnode import Tag, HTMLNode


class TestTextNode(TestCase):
    def test_default_properties(self):
        self.assertEqual(HTMLNode(), HTMLNode(tag=None, value=None, children=None, props=None))

    def test_all_properties(self):
        children_node = HTMLNode()
        node = HTMLNode(Tag.P, "This is a paragraph", [children_node], {"class": "my_class"}) 
        self.assertEqual(str(node), "HTMLNode(tag=<Tag.P: 'p'>, value='This is a paragraph', children=[HTMLNode(tag=None, value=None, children=None, props=None)], props={'class': 'my_class'})")

    def test_tag_isnot_Tag_object(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(tag="p") # type: ignore

    def test_value_isnot_str(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(value=12) # type: ignore

    def test_children_isnot_list(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(children=HTMLNode()) # type: ignore

    def test_props_isnot_dict(self):
        with self.assertRaises(TypeError):
              node = HTMLNode(props="dict"), # type: ignore

    def test_props_to_html(self):
        node = HTMLNode(tag=Tag.A, 
                   props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

        
if __name__ == '__main__':
    main()