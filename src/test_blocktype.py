import unittest

from blocktype import BlockType, block_to_block_type

class Testsplitnode(unittest.TestCase):

    def test_blocktype_paragraph(self):
        md = "this should just be a paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_header_1(self):
        md = "# this should be a header"
        self.assertEqual(block_to_block_type(md), BlockType.heading)

    def test_blocktype_header_2(self):
        md = "## this should also be a header"
        self.assertEqual(block_to_block_type(md), BlockType.heading)

    def test_blocktype_not_a_header(self):
        md = "######## this should not be a header but a paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_not_a_header_no_space(self):
        md = "####this should not be a header but a paragraph"
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_code(self):
        md = "``` this should be some code ```"
        self.assertEqual(block_to_block_type(md), BlockType.code)

    def test_blocktype_not_code(self):
        md = "`` this should be a paragraph looking like code ```"
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_code_but_looks_like_header(self):
        md = "``` ### this should be a code but has hashes ```"
        self.assertEqual(block_to_block_type(md), BlockType.code)

    def test_blocktype_quote_one_line(self):
        md = ">this is a quote"
        self.assertEqual(block_to_block_type(md), BlockType.quote)

    def test_blocktype_quote_two_line(self):
        md = """>this is a quote 
>and so is this"""
        self.assertEqual(block_to_block_type(md), BlockType.quote)

    def test_blocktype_quote_two_line_no_quote(self):
        md = """ >this is a quote 
should now be a paragraph"""
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_unordered_list(self):
        md = """- this is a list line 
- so is this"""
        self.assertEqual(block_to_block_type(md), BlockType.unordered_list)

    def test_blocktype_unordered_list_but_broke(self):
        md = """- this is a list line 
this is not"""
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_ordered_list(self):
        md = """1. this is a list line 
2. so is this
3. so is this"""
        self.assertEqual(block_to_block_type(md), BlockType.ordered_list)

    def test_blocktype_ordered_list_but_borke(self):
        md = """1. this is a list line 
2. so is this
56. but this is the wrong number"""
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

    def test_blocktype_ordered_list_but_borke(self):
        md = ""
        self.assertEqual(block_to_block_type(md), BlockType.paragraph)

if __name__ == "__main__":
    unittest.main()