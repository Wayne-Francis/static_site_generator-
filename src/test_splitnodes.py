import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        new_nodes,
    )
        
    def test_split_no_images(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
            ],
        new_nodes,
    )
        
    def test_split_images_everywhere(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) wow image first ![second image](https://img.example.com/map.png) then a second one and look a third ![third image](https://img.example.com/snacks.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" wow image first ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://img.example.com/map.png"),
                TextNode(" then a second one and look a third ", TextType.TEXT),
                TextNode("third image", TextType.IMAGE, "https://img.example.com/snacks.jpg")
            ],
        new_nodes,
    )
        
    def test_split_2_images_in_a_row(self):
        node = TextNode(
            "look two images in a row! ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://img.example.com/map.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("look two images in a row! ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://img.example.com/map.png")
            ],
        new_nodes,
    )
        
    def test_split_images_no_text_node(self):
        node = TextNode(
            "Not a text node ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.IMAGE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Not a text node ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.IMAGE),
    
            ],
        new_nodes,
    )
        
    def test_split_images_mixed_nodes(self):
        nodes = [
            TextNode("A ![one](u1) X", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "u-img"),
            TextNode("B ![two](u2)", TextType.TEXT),
            TextNode("link", TextType.LINK, "u-link"),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "u1"),
            TextNode(" X", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "u-img"),
            TextNode("B ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "u2"),
            TextNode("link", TextType.LINK, "u-link"),
        ]
        self.assertListEqual(expected, result)
        
    def test_split_Links(self):
        node = TextNode(
            "Visit [the library](https://example.com/library) and [the armory](https://example.com/armory) today.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
        TextNode("Visit ", TextType.TEXT),
        TextNode("the library", TextType.LINK, "https://example.com/library"),
        TextNode(" and ", TextType.TEXT),
        TextNode("the armory", TextType.LINK, "https://example.com/armory"),
        TextNode(" today.", TextType.TEXT),
            ],new_nodes)
        
    def test_split_Links_at_start(self):
        node = TextNode(
            "[the library](https://example.com/library) is great",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
        TextNode("the library", TextType.LINK, "https://example.com/library"),
        TextNode(" is great", TextType.TEXT),
            ],new_nodes)
    
    def test_split_Links_adjacent(self):
        node = TextNode(
            "[the library](https://example.com/library)[the arcade](https://example.com/arcade) are great",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
        TextNode("the library", TextType.LINK, "https://example.com/library"),
        TextNode("the arcade", TextType.LINK, "https://example.com/arcade"),
        TextNode(" are great", TextType.TEXT),
            ],new_nodes)
        
    def test_split_Links_start_middle_end(self):
        node = TextNode(
            "[the library](https://example.com/library) and [the arcade](https://example.com/arcade) and [the pub](https://example.com/pub) are great",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
        TextNode("the library", TextType.LINK, "https://example.com/library"),
        TextNode(" and ", TextType.TEXT),
        TextNode("the arcade", TextType.LINK, "https://example.com/arcade"),
        TextNode(" and ", TextType.TEXT),
        TextNode("the pub", TextType.LINK, "https://example.com/pub"),
        TextNode(" are great", TextType.TEXT),
            ],new_nodes)
        
    def test_split_Links_with_punctuations(self):
        node = TextNode(
            "Visit [the library](https://example.com/library) today! and maybe? [the armory](https://example.com/armory) !today!.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
        TextNode("Visit ", TextType.TEXT),
        TextNode("the library", TextType.LINK, "https://example.com/library"),
        TextNode(" today! and maybe? ", TextType.TEXT),
        TextNode("the armory", TextType.LINK, "https://example.com/armory"),
        TextNode(" !today!.", TextType.TEXT),
            ],new_nodes)
    
    # python
    def test_split_links_mixed_nodes(self):
        nodes = [
            TextNode("A [one](u1) X", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "u-img"),
            TextNode("B [two](u2)", TextType.TEXT),
            TextNode("link", TextType.LINK, "u-link"),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.LINK, "u1"),
            TextNode(" X", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "u-img"),
            TextNode("B ", TextType.TEXT),
            TextNode("two", TextType.LINK, "u2"),
            TextNode("link", TextType.LINK, "u-link"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_no_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_no_delim(self):
        text = "This is text with an italic word and a code block and an image and a link"
        result = text_to_textnodes(text)
        expected = [
        TextNode("This is text with an italic word and a code block and an image and a link", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_delims(self):
        text = "**text**_italic_`code block`![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
        TextNode("text", TextType.BOLD),
        TextNode("italic", TextType.ITALIC),
        TextNode("code block", TextType.CODE),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_single_delim(self):
        text = "_text__italic__codeblock__obiwan__link_"
        result = text_to_textnodes(text)
        expected = [
        TextNode("text", TextType.ITALIC),
        TextNode("italic", TextType.ITALIC),
        TextNode("codeblock", TextType.ITALIC),
        TextNode("obiwan", TextType.ITALIC),
        TextNode("link", TextType.ITALIC),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_unmatched_delim(self):
        text = "This is text with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(Exception) as context: 
            result = text_to_textnodes(text)
            self.assertEqual(str(context.exception), "invalid Markdown syntax")

                
if __name__ == "__main__":
    unittest.main()