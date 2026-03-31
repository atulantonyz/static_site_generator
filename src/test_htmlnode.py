import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p","This is an html node",props = {"href": "https://www.boot.dev.com"})

        self.assertEqual( ' href="https://www.boot.dev.com"', node.props_to_html())


    def test_repr(self):
        node = HTMLNode(tag = "p",value = "This is a html node")
        self.assertEqual(
            "HTMLNode(p, This is a html node, children: None, None)", repr(node)
        )

    def test_repr2(self):
        cnode1 = HTMLNode("p","This is a child node")
        cnode2 = HTMLNode("p","This is a child node")
        node = HTMLNode("p","This is a html node",children = [cnode1, cnode2])
        self.assertEqual(
            f"HTMLNode(p, This is a html node, children: [{repr(cnode1)}, {repr(cnode2)}], None)",repr(node)
        )
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
