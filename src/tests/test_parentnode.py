import pytest

from htmlnode import Tag
from leafnode import LeafNode
from parentnode import ParentNode


def test_to_html_no_tag():
    with pytest.raises(ValueError):
        ParentNode(tag=None, children=[LeafNode(None, "Value")]).to_html()

def test_to_html_no_children():
    with pytest.raises(ValueError):
        ParentNode(Tag.UL, children=[]).to_html()

def test_to_html_no_nested_levels():
    node_a = LeafNode(Tag.A, "I am a hyperlink", {"href": "https//myawesomelink.net", "target": "_blank"})
    node_p = ParentNode(Tag.P, [node_a]) # top-parent
    assert node_p.to_html() == '<p><a href="https//myawesomelink.net" target="_blank">I am a hyperlink</a></p>'


def test_to_html_three_nested_levels_with_props_with_several_children():
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


