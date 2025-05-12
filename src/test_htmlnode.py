import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        node2 = HTMLNode()
        node2.tag = "a"
        node2.value = "link"
        node2.children = None
        node2.props = {"href": "https://www.google.com",
                       "target": "_blank",}
        node_repr = f"{node}"
        node2_repr = f"{node2}"
        self.assertEqual(node_repr, node2_repr)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com",
                               "target": "_blank",})
        self.assertEqual(node.props_to_html(),
                         " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html2(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        self.assertEqual(node.props_to_html(),
                         " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html3(self):
        node = HTMLNode("div", "centered", None, {"class":"centered"})
        self.assertEqual(node.props_to_html(),
                         " class=\"centered\"")
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_init_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "centered"})
        props = node.props_to_html()
        self.assertEqual(props, " class=\"centered\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_childrens(self):
        node = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
        self.assertEqual(node.to_html(),
                        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>" )

    def test_to_html_with_children_and_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text", {"class":"title"}),
                LeafNode(None, "Just a normal text"),
                LeafNode("i", "italic text", {"class": "my-italic"}),
            ],
            {"class": "centered"}
        )
        self.assertEqual(node.to_html(),
                         '<div class="centered"><b class="title">Bold text</b>Just a normal text<i class="my-italic">italic text</i></div>')


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(html_node.value, "This is a link")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"}
        )
