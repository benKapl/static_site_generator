from splitblocks import BlockType, markdown_to_blocks, block_to_block_type

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

    def test_delete_xa0(self):
        markdown = """We write Big-O notation like this: `O(formula)`

Where `formula` describes how an algorithm's run time or space requirements grow **as the input size grows.**"""
        expected_output = ['We write Big-O notation like this: `O(formula)`',
                           "Where `formula` describes how an algorithm's run time or space requirements "
                           "grow **as the input size grows.**"]
        assert markdown_to_blocks(markdown) == expected_output


class TestBlockToBlockType:
    def test_is_heading_true(self):
        input_case = "###### # This is another heading"
        assert block_to_block_type(input_case) == BlockType.HEADING

    def test_is_heading_false(self):
        input_case = "##This is NOT a heading"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH
 
    def test_is_code_true(self):
        input_case = "```###### # Despite it's look, it's code my friend```"
        assert block_to_block_type(input_case) == BlockType.CODE

    def test_is_code_false(self):
        input_case = "```##This is NOT a CODE``"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH

    def test_is_quote_true(self):
        input_case = "> ```##This isQUOTE\n> NOT code```"
        assert block_to_block_type(input_case) == BlockType.QUOTE

    def test_is_quote_false(self):
        input_case = "> This \n>IS NOT\nquote"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH

    def test_is_unordered_list_true(self):
        input_case = "* ```##This is unordered list\n- > my friend```"
        assert block_to_block_type(input_case) == BlockType.UNORDERED_LIST

    def test_is_unordered_list_false(self):
        input_case = "* Did you forget\n-A space ?"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH

    def test_is_ordered_list_true(self):
        input_case = "1. Ordered list\n2. Are hard to check\n3. don't you think ?`"
        assert block_to_block_type(input_case) == BlockType.ORDERED_LIST

    def test_is_ordered_list_false_wrong_number(self):
        input_case = "1. Ordered list\n2. Are hard to check\n4. SHOULD BE '3' !!"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH

    def test_is_ordered_list_false_wrong_spacing(self):
        input_case = "1. Ordered list\n2. \n3.No space !!"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH

    def test_is_ordered_list_false_no_point(self):
        input_case = "1 Ordered list\n2. Are sad\n3.with no point !!"
        assert block_to_block_type(input_case) == BlockType.PARAGRAPH


