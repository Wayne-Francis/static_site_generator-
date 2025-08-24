from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)
        
    def test_to_html_parent_node_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None,[child_node])
        with self.assertRaises(ValueError) as context: 
            parent_node.to_html()
        self.assertEqual(str(context.exception), "No Tag given")

    def test_to_html_parent_node_no_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div",None)
        with self.assertRaises(ValueError) as context: 
            parent_node.to_html()
        self.assertEqual(str(context.exception), "parentnode must have child node")
    
    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("span", "child", props = {"class": "highlight"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span class="highlight">child</span></div>')

    def test_to_html_parent_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

    def test_to_html_parent_node_empty_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div",[])
        with self.assertRaises(ValueError) as context: 
            parent_node.to_html()
        self.assertEqual(str(context.exception), "parentnode must have child node")

    def test_to_html_with_great_grandchildren(self):
        great_great_grandchild_node = LeafNode("d" ,"great_great_grandchild")
        great_grandchild_node = ParentNode("c", [great_great_grandchild_node])
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><c><d>great_great_grandchild</d></c></b></span></div>",)
        
    def test_to_html_multiple_children_same_level(self):
        child1 = LeafNode("span", "First")
        child2 = LeafNode("b", "Second") 
        child3 = LeafNode("i", "Third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), "<div><span>First</span><b>Second</b><i>Third</i></div>")

    def test_to_html_mixed_child_types(self):
        leaf_child = LeafNode("span", "I'm a leaf")
        grandchild = LeafNode("b", "nested")
        parent_child = ParentNode("p", [grandchild])
        another_leaf = LeafNode("i", "Another leaf")
        mixed_parent = ParentNode("div", [leaf_child, parent_child, another_leaf])
        self.assertEqual(mixed_parent.to_html(), "<div><span>I'm a leaf</span><p><b>nested</b></p><i>Another leaf</i></div>")


if __name__ == "__main__":
    unittest.main()
