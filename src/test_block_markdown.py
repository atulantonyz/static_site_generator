import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType,markdown_to_html_node

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


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headings(self):
        md = """
### This is a heading text in a h3 tag here

#### This is another text in a h4 tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading text in a h3 tag here</h3><h4>This is another text in a h4 tag here</h4></div>",
        )
    def test_quotetext(self):
        md = """
> This is a quote text

>This is another quote text with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote text</blockquote><blockquote>This is another quote text with <i>italic</i> text and <code>code</code> here</blockquote></div>",
        )
    def test_uo_list(self):
        md ="""
- Fast and lightweight
- Easy to configure
- Cross-platform support
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Fast and lightweight</li><li>Easy to configure</li><li>Cross-platform support</li></ul></div>",
        )

    def test_o_list(self):
        md ="""
1. Write the failing test
2. Implement the feature
3. Refactor and clean up
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Write the failing test</li><li>Implement the feature</li><li>Refactor and clean up</li></ol></div>",
        )
    
    def test_heading_and_paragraph(self):
        md = """
## Getting Started

This is a **bold** intro paragraph with some `inline code` here.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Getting Started</h2><p>This is a <b>bold</b> intro paragraph with some <code>inline code</code> here.</p></div>",
        )

    def test_heading_and_unordered_list(self):
        md = """
## Features

- Fast and _lightweight_
- Easy to configure
- Cross-platform support
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Features</h2><ul><li>Fast and <i>lightweight</i></li><li>Easy to configure</li><li>Cross-platform support</li></ul></div>",
        )

    def test_quote_and_ordered_list(self):
        md = """
> Always write tests before shipping.

1. Write the failing test
2. Implement the feature
3. Refactor and clean up
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Always write tests before shipping.</blockquote><ol><li>Write the failing test</li><li>Implement the feature</li><li>Refactor and clean up</li></ol></div>",
        )

    def test_heading_paragraph_and_code(self):
        md = """
## Quick Start

Run the following command to get started:

```
npm install my-package
const app = require('my-package');
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Quick Start</h2><p>Run the following command to get started:</p><pre><code>npm install my-package\nconst app = require('my-package');\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
