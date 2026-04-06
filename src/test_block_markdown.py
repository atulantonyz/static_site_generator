import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

class TestBlocktoBlockType(unittest.TestCase):
    def test_heading_block(self):

        heading_block="""
        # Welcome to the Docs
        """.strip()
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):

        code_block ="""
        ```
        bash
        npm install my-package```
        """.strip()
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block(self):

        quote_block ="""
        > Always write tests before shipping to production.
        """.strip()
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_uolist_block(self):

        uolist_block ="""
        - Fast and lightweight
        - Easy to configure
        - Cross-platform support
        """.strip()
        block_type = block_to_block_type(uolist_block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_olist_block(self):

        olist_block ="""
        1. Write the failing test
        2. Implement the feature
        3. Refactor and clean up
        """.strip()
        block_type = block_to_block_type(olist_block)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_para_block(self):

        para_block="""
        This is an introductory paragraph that explains the purpose of this documentation.
        """.strip()
        block_type = block_to_block_type(para_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)




if __name__ == "__main__":
    unittest.main()
