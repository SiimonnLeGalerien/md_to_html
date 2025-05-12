from textnode import TextNode
from htmlnode import HTMLNode


def main():
    textnode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(textnode)
    htmlnode = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank",
    })
    htmlnode.props_to_html()

main()
