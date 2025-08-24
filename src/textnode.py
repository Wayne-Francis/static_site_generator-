from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
   TEXT = "text"
   BOLD = "bold"
   ITALIC = "italic"
   CODE = "code"
   LINK = "link"
   IMAGE = "image"

class TextNode():
   
   def __init__(self,text,text_type,url=None):
    self.text = text
    self.text_type = text_type
    self.url = url   

   def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
   
   def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
   
def text_node_to_html_node(text_node):
   allowed_types = (TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE)
   if text_node.text_type not in allowed_types:
      raise Exception("invalid text type")
   if text_node.text_type == TextType.TEXT:
      just_text = LeafNode(tag=None, value = text_node.text, props = None)
      return just_text
   if text_node.text_type == TextType.BOLD:
      bold = LeafNode(tag="b",value = text_node.text, props = None)
      return bold
   if text_node.text_type == TextType.ITALIC:
      italic = LeafNode(tag="i",value = text_node.text, props = None)
      return italic 
   if text_node.text_type == TextType.CODE:
      code = LeafNode(tag="code",value = text_node.text, props = None)
      return code 
   if text_node.text_type == TextType.LINK:
      link = LeafNode(tag="a",value = text_node.text, props = {"href":text_node.url})
      return link
   if text_node.text_type == TextType.IMAGE:
      image = LeafNode(tag="img",value = "", props = {"src":text_node.url, "alt": text_node.text})
      return image
    