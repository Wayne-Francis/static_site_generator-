import unittest

from extractmarkdown import  extract_markdown_images, extract_markdown_links

class Testextractmarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev","https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "Here's ![first](url1.jpg) and ![second](url2.png) and ![third](url3.gif)"
        )
        self.assertListEqual([
            ("first", "url1.jpg"),
            ("second", "url2.png"), 
            ("third", "url3.gif")
        ], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images at all")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Visit [Google](https://google.com) or [GitHub](https://github.com) today"
        )
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)

    def test_mixed_images_and_links(self):
    # Test that links function doesn't pick up images
        matches = extract_markdown_links(
            "Here's an ![image](img.jpg) and a [link](site.com)"
        )
        self.assertListEqual([("link", "site.com")], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images("Empty alt: ![](https://example.com/image.jpg)")
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)


if __name__ == "__main__":
    unittest.main()