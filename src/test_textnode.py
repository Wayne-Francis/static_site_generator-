import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_nodes_with_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text node", TextType.BOLD, url = "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_nodes_with_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text node", TextType.ITALIC, url = None)
        self.assertNotEqual(node, node2)

    def test_nodes_with_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text", TextType.BOLD, url = None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "plain text")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("bold!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold!")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("emphasis", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "emphasis")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("x = 5", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x = 5")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("Bear", TextType.IMAGE, url="bear.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "bear.jpg", "alt": "Bear"})

if __name__ == "__main__":
    unittest.main()