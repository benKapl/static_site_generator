import pytest

from page_formatter import (text_to_textnodes, 
                            text_node_to_html_node,
                            markdown_to_html_node,
                            get_heading_tag,
                            format_markdown_heading,
                            format_markdown_code,
                            format_markdown_quote,
                            markdown_lists_to_li_nodes,
                            extract_title)
 
from textnode import TextType, TextNode
from htmlnode import Tag, ParentNode, LeafNode


class TestTextToTextNodes:

    def test_all_cases(self):
        input_text = """This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        assert text_to_textnodes(input_text) == expected_output

    def test_several_bold_delimiters(self):
        input_text = "This is **bold text** and **another bold** section."
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" section.", TextType.TEXT)
]
        assert text_to_textnodes(input_text) == expected_output

    def test_entire_text_italic(self):
        input_text = "*entire text as italic*"
        assert text_to_textnodes(input_text) == [TextNode("entire text as italic", TextType.ITALIC)]

    def test_multiple_images(self):
        input_text = "This is an image ![first image](http://example.com/1.jpg) and another image ![second image](http://example.com/2.jpg)."
        expected_output = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("first image", TextType.IMAGE, "http://example.com/1.jpg"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "http://example.com/2.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        assert text_to_textnodes(input_text) == expected_output

    def test_entire_text_link(self):
        input_text = "[Boot.dev](https://boot.dev)"
        assert text_to_textnodes(input_text) == [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")]

    def test_input_is_textnode(self):
        pass


class TestTextNodeToHtmlNode:
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


class TestMarkdownToHtmlNode:
    def test_big_markdown_document(self):
        input_text = """> Documentation
> - [Wikipedia](https://en.wikipedia.org/wiki/NP_(complexity)) 
> - [Vidéo](https://youtu.be/zVLSrrIKKF0)

`NP` (which stands for [nondeterministic polynomial time](https://en.wikipedia.org/wiki/NP_(complexity)) is the set of problems whose solutions can be _verified_ in [polynomial time](app://obsidian.md/Polynomial%20Time%20=%20P), but not necessarily _solved_ in polynomial time.

## P is in NP

Because all problems that can be _solved_ in polynomial time can also be _verified_ in polynomial time, all the problems in `P` are also in `NP`.

![P in NP](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/vO4GfRb.png)

### The Oracle

A good way of thinking about problems in `NP` is to imagine that we have a magic oracle that gives us potential solutions to problems. Here would be our **process** for finding if a problem is in `NP`:

- Present the problem to the **magic oracle**
- The magic oracle gives us a *potential solution*
- We verify in polynomial time that the solution is correct

```python
foo = "random code to prove code block works"
print(foo)
# result of foo
```

If we can do the verification in polynomial time, the problem is in `NP`, otherwise, it isn't.

#### Example of NP problems

- [Cryptography](app://obsidian.md/Cryptography) :
- [Traveling Salesman Problem](app://obsidian.md/Traveling%20Salesman%20Problem)
"""


        expected = """<div><blockquote>Documentation<br>- <a href="https://en.wikipedia.org/wiki/NP_(complexity">Wikipedia</a>) <br>- <a href="https://youtu.be/zVLSrrIKKF0">Vidéo</a></blockquote><p><code>NP</code> (which stands for <a href="https://en.wikipedia.org/wiki/NP_(complexity">nondeterministic polynomial time</a>) is the set of problems whose solutions can be _verified_ in <a href="app://obsidian.md/Polynomial%20Time%20=%20P">polynomial time</a>, but not necessarily _solved_ in polynomial time.</p><h2>P is in NP</h2><p>Because all problems that can be _solved_ in polynomial time can also be _verified_ in polynomial time, all the problems in <code>P</code> are also in <code>NP</code>.</p><p><img src="https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/vO4GfRb.png" alt="P in NP"></img></p><h3>The Oracle</h3><p>A good way of thinking about problems in <code>NP</code> is to imagine that we have a magic oracle that gives us potential solutions to problems. Here would be our <b>process</b> for finding if a problem is in <code>NP</code>:</p><ul><li>Present the problem to the <b>magic oracle</b></li><li>The magic oracle gives us a <i>potential solution</i></li><li>We verify in polynomial time that the solution is correct</li></ul><pre><code>foo = "random code to prove code block works"
print(foo)
# result of foo</code></pre><p>If we can do the verification in polynomial time, the problem is in <code>NP</code>, otherwise, it isn't.</p><h4>Example of NP problems</h4><ul><li><a href="app://obsidian.md/Cryptography">Cryptography</a> :</li><li><a href="app://obsidian.md/Traveling%20Salesman%20Problem">Traveling Salesman Problem</a></li></ul></div>"""
        assert markdown_to_html_node(input_text).to_html() == expected


class TestHelperFunctions:
    def test_get_heading_tag(self):
        assert get_heading_tag("# Heading") == Tag.H1
        assert get_heading_tag("## Subheading") == Tag.H2
        assert get_heading_tag("### Subsubheading") == Tag.H3
        assert get_heading_tag("#### Subsubsubheading") == Tag.H4
        assert get_heading_tag("##### Subsubsubsubheading") == Tag.H5
        assert get_heading_tag("###### Subsubsubsubsubheading") == Tag.H6

    def test_format_markdown_heading(self):
        assert format_markdown_heading("# Heading") == "Heading"
        assert format_markdown_heading("## Subheading") == "Subheading"
        assert format_markdown_heading("### #### Someone made a space") == "#### Someone made a space"

    def test_format_markdown_code(self):
        assert format_markdown_code("```python\nprint('hello')\n```") == "print('hello')"
        assert format_markdown_code("```\nprint('hello')\n```") == "print('hello')"
        with pytest.raises(Exception):
            format_markdown_code("``issue = 'two_ticks_first_line'\n````")
        with pytest.raises(Exception):
            format_markdown_code("````issue = 'one_tick_last_line'\n`")

    def test_format_markdown_quote(self):
        assert format_markdown_quote("> quote") == "quote"
        assert format_markdown_quote("> quote\n> another line") == "quote<br>another line"

    def test_markdown_lists_to_li_nodes_NORMAL_UL(self):
        text = "- Coucou\n- je suis\n- une liste normale"
        expected = ("[ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=Coucou, children=None, props=None)], props=None), '
 "ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=je suis, children=None, props=None)], props=None), '
 "ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=une liste normale, children=None, props=None)], props=None)]')
        assert str(markdown_lists_to_li_nodes(text, 2)) == expected

    def test_markdown_lists_to_li_nodes_OL_WITH_BOLD(self):
        text = "1. Je suis\n2. une liste ordonnée\n3. avec **du gras**"
        expected = ("[ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=Je suis, children=None, props=None)], props=None), '
 "ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=une liste ordonnée, children=None, props=None)], props=None), '
 "ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 "value=avec , children=None, props=None), LeafNode(tag=<Tag.B: 'b'>, value=du "
 'gras, children=None, props=None)], props=None)]')
        assert str(markdown_lists_to_li_nodes(text, 3)) == expected

    def test_markdown_lists_to_li_nodes_UL_WRONG_INDEX(self):
        text = "- Ligne"
        expected = ("[ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value=igne, children=None, props=None)], props=None)]')
        assert str(markdown_lists_to_li_nodes(text, 3)) == expected

    def test_markdown_lists_to_li_nodes_OL_WRONG_INDEX(self):
        text = "1. Un\n2. Deux"
        expected = ("[ParentNode(tag=<Tag.LI: 'li'>, value=None, children=[LeafNode(tag=None, "
 'value= Un, children=None, props=None)], props=None), ParentNode(tag=<Tag.LI: '
 "'li'>, value=None, children=[LeafNode(tag=None, value= Deux, children=None, "
 'props=None)], props=None)]')
        assert str(markdown_lists_to_li_nodes(text, 2)) == expected


class TestExtractMarkdownTitle:
    def test_valid_title_one_line(self):
        markdown = "# Title"
        assert extract_title(markdown) == "Title"

    def test_valid_title_multiple_lines(self):
        markdown = "# Title\n\nParagraph"
        assert extract_title(markdown) == "Title"

    def test_invalid_title_h3(self):
        markdown = "### Title\n\nParagraph"
        with pytest.raises(Exception) as e:
            extract_title(markdown)

    def test_invalid_title_h2_then_h1(self):
        markdown = "## Title\n# Another Title\n\nParagraph"
        with pytest.raises(Exception) as e:
            extract_title(markdown)