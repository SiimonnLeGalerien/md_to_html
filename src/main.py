from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parser import split_nodes_image, markdown_to_html_node
from block import BlockType, block_to_block_type

def main():
    markdown = """
# Article 1

blah blah blah
blah blah

> quoted
> text

0. item 0
1. item 1

- item one
- item two"""

    html = markdown_to_html_node(markdown)
    print(html.to_html())
main()
