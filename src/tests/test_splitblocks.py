from splitblocks import markdown_to_blocks

import pytest

class TestMarkdownToBlocks:
    def test_single_block(self):
        markdown = "# This is a heading"
        expected_output = ["# This is a heading"]
        assert markdown_to_blocks(markdown) == expected_output

    def test_multiple_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        assert markdown_to_blocks(markdown) == expected_output

    def test_empty_string(self):
        markdown = ""
        expected_output = []
        assert markdown_to_blocks(markdown) == expected_output

    def test_whitespace_only(self):
        markdown = "\n\n\n"
        expected_output = []
        assert markdown_to_blocks(markdown) == expected_output
