from htmlnode import HTMLNode, LeafNode

import unittest


class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props = {"class": "highlight", "id": "intro Welcome to my website" })
        self.assertEqual(node.props_to_html(), ' class="highlight" id="intro Welcome to my website"')
        
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_none_props(self):
        node = HTMLNode(props = None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_no_prop(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_a_with_prop(self):
        node = LeafNode("a", "Hello, world!", props = {"class": "highlight"})
        self.assertEqual(node.to_html(), '<a class="highlight">Hello, world!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_raises_valueerror(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()
    
    def test_leaf_to_html_a_with_multiple_props_any_order(self):
        node = LeafNode("a", "Hello, world!", props={"class": "highlight", "id": "intro"})
        html = node.to_html()
        # Check the tag structure
        self.assertTrue(html.startswith('<a') and html.endswith('>Hello, world!</a>'))
        # Check each attribute is present somewhere in the tag
        self.assertIn('class="highlight"', html)
        self.assertIn('id="intro"', html)
    

if __name__ == "__main__":
    unittest.main()
