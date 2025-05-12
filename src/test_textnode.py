import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an other text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_self_without_url(self):
        node = TextNode("link", TextType.LINK)
        node2 = TextNode("link", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_other_without_url(self):
        node = TextNode("link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("link", TextType.LINK)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
