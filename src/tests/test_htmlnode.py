import pytest
from unittest import main, TestCase

from htmlnode import Tag, HTMLNode, LeafNode, ParentNode


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


class TestParentNode:
    def test_to_html_no_tag(self):
        with pytest.raises(ValueError):
            ParentNode(tag=None, children=[LeafNode(None, "Value")]).to_html() # type: ignore

    def test_to_html_no_children(self):
        with pytest.raises(ValueError):
            ParentNode(Tag.UL, children=[]).to_html()

    def test_to_html_no_nested_levels(self):
        node_a = LeafNode(Tag.A, "I am a hyperlink", {"href": "https//myawesomelink.net", "target": "_blank"})
        node_p = ParentNode(Tag.P, [node_a]) # top-parent
        assert node_p.to_html() == '<p><a href="https//myawesomelink.net" target="_blank">I am a hyperlink</a></p>'

    def test_to_html_three_nested_levels_with_props_with_several_children(self):
        node_a = LeafNode(Tag.A, "I am a hyperlink", {"href": "https//myawesomelink.net", "target": "_blank"})
        node_raw_1 = LeafNode(None, "raw text")
        node_raw_2 = LeafNode(None, "Another raw text")
        node_i = LeafNode(Tag.I, "This is italic")
        node_b = LeafNode(Tag.B, "BOLDMAN !") #3rd level child
        node_li_1 = ParentNode(Tag.LI, [node_raw_1, node_b]) # 2nd level nest child
        node_li_2 = ParentNode(Tag.LI, [node_raw_2, node_a]) # 2nd level nest child
        node_ul = ParentNode(Tag.UL, [node_li_1, node_li_2]) # 1st level nested child
        node_p = ParentNode(Tag.P, [node_ul, node_i]) # top-parent

        assert node_p.to_html() == '<p><ul><li>raw text<b>BOLDMAN !</b></li><li>Another raw text<a href="https//myawesomelink.net" target="_blank">I am a hyperlink</a></li></ul><i>This is italic</i></p>'
        
if __name__ == '__main__':
    main()