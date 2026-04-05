import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes[0])
        self.assertEqual(TextNode("code block",TextType.CODE),new_nodes[1])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes[2])

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes[0])
        self.assertEqual(TextNode("bold",TextType.BOLD),new_nodes[1])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes[2])

    def test_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes[0])
        self.assertEqual(TextNode("italic",TextType.ITALIC),new_nodes[1])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes[2])

    def test_multiple(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1,node2,node3], "`",TextType.CODE)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes[0])
        self.assertEqual(TextNode("code block",TextType.CODE),new_nodes[1])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes[2])
        self.assertEqual(node2,new_nodes[3])
        self.assertEqual(node3,new_nodes[4])

    def test_successive(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1,node2,node3], "`",TextType.CODE)
        new_nodes1 = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes1,"_",TextType.ITALIC)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes2[0])
        self.assertEqual(TextNode("code block",TextType.CODE),new_nodes2[1])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes2[2])
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes2[3])
        self.assertEqual(TextNode("bold",TextType.BOLD),new_nodes2[4])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes2[5])
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes2[6])
        self.assertEqual(TextNode("italic",TextType.ITALIC),new_nodes2[7])
        self.assertEqual(TextNode(" word",TextType.TEXT),new_nodes2[8])

    def test_simultaneous(self):
        node = TextNode("This is text with a `code block` word, **bold** word, and an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`",TextType.CODE)
        new_nodes1 = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes1,"_",TextType.ITALIC)
        self.assertEqual(TextNode("This is text with a ",TextType.TEXT),new_nodes2[0])
        self.assertEqual(TextNode("code block",TextType.CODE),new_nodes2[1])
        self.assertEqual(TextNode(" word, ",TextType.TEXT),new_nodes2[2])
        self.assertEqual(TextNode("bold",TextType.BOLD),new_nodes2[3])
        self.assertEqual(TextNode(" word, and an ",TextType.TEXT),new_nodes2[4])
        self.assertEqual(TextNode("italic",TextType.ITALIC),new_nodes2[5])

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev") ], matches)


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
