print("hello world")

import os
from textnode import *

def copy_contents(public_directory,static_directory, file_path):

    abs_public = os.path.abspath(public_directory) # creates the abs path to the work
    abs_file_path = os.path.abspath(os.path.join(abs_public, file_path)) # this could be useful for later 
    public_path_exists = os.path.exists(abs_public) # creates a boolean varable to determine the public directory exists 
    if public_path_exists:
        



def main():
    textnode = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(textnode)

main()

