import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class Testsplitnode(unittest.TestCase):

    def test_normal(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
    TextNode("This is ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" text", TextType.TEXT),
    ])
        
    def test_empty_normal_text(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
    TextNode("bold", TextType.BOLD)
    ])
        
    def test_unmatched_delimiter(self):
        node = TextNode("text **bold", TextType.TEXT)
        with self.assertRaises(Exception) as context: 
            new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(str(context.exception), "invalid Markdown syntax")

    def test_empty_non_txt_node(self):
        node = TextNode("**bold**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
    TextNode("**bold**", TextType.BOLD)
    ])
        
    def test_normal_code_block(self):
        node = TextNode("This is `code block` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" text", TextType.TEXT),
    ])
        
if __name__ == "__main__":
    unittest.main()