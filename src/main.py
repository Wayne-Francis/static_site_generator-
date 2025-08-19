print("hello world")

from textnode import *

def main():
    textnode = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(textnode)

main()

