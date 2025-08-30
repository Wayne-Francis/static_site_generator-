
import unittest

from markdown_to_blocks import markdown_to_blocks

class Testsplitnode(unittest.TestCase):

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

    def test_markdown_to_blocks_empty(self):
        md = ""
        self.assertEqual(markdown_to_blocks(md), [])
    
    def test_markdown_to_blocks_whitespace_only(self):
        md = "   \n\t\n  "
        self.assertEqual(markdown_to_blocks(md), [])

    def test_markdown_to_blocks_extra_blank_lines_between_blocks(self):
        md = "a\n\n\n\nb"
        self.assertEqual(markdown_to_blocks(md), ["a","b"])

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = "\n\na\n\nb\n\n"
        self.assertEqual(markdown_to_blocks(md), ["a","b"])

    def test_markdown_to_blocks_single_line(self):
        md = "this is a single line"
        self.assertEqual(markdown_to_blocks(md), ["this is a single line"])


if __name__ == "__main__":
    unittest.main()