import unittest

from block_to_html import markdown_to_html_node, strip_headers_count

class Testsplitnode(unittest.TestCase):

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
        
    def test_quotes(self):
            md = """
>this is a quote
>and so is this

>This quote has an _italic_ word and a **bolded** word here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
        "<div><blockquote>this is a quote and so is this</blockquote><blockquote>This quote has an <i>italic</i> word and a <b>bolded</b> word here</blockquote></div>",
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
        
    def test_another_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
this is also the _same_
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\nthis is also the _same_\n</code></pre></div>",
    )
        
    def test_ordered_list(self):
        md = """
1. this is a list line  
2. so is this 
3. so is this  
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ol><li>this is a list line</li><li>so is this</li><li>so is this</li></ol></div>",
    )
        
    def test_unordered_list(self):
        md = """
- this is a list line  
- so is this 
- so is this  
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ul><li>this is a list line</li><li>so is this</li><li>so is this</li></ul></div>",
    )
        
    def test_strip_headers_count(self):
        md = "# Title"
        result = strip_headers_count(md)
        self.assertEqual(result, [(1, "Title")])

    # python
    def test_headings(self):
        md = """
# Title One

### A _fancy_ title

###### Deep Title with **bold**

###NoSpace
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>Title One</h1><h3>A <i>fancy</i> title</h3><h6>Deep Title with <b>bold</b></h6><p>###NoSpace</p></div>",
    )

if __name__ == "__main__":
    unittest.main()