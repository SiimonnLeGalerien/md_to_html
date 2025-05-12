import unittest
from htmlnode import HTMLNode


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
                         "href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html2(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        self.assertEqual(node.props_to_html(),
                         "href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html3(self):
        node = HTMLNode("div", "centered", None, {"class":"centered"})
        self.assertEqual(node.props_to_html(),
                         "class=\"centered\"")
