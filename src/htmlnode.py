from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

def text_node_to_html_node(text_node):
    match (text_node.text_type):
       case(TextType.TEXT):
           return LeafNode(None, text_node.text)
       case(TextType.BOLD):
           return LeafNode("b", text_node.text)
       case(TextType.ITALIC):
           return LeafNode("i", text_node.text)
       case(TextType.CODE):
           return LeafNode("code", text_node.text)
       case(TextType.LINK):
           return LeafNode("a", text_node.text,{"href":text_node.url})
       case(TextType.IMAGE):
           return LeafNode("img", "", {"src":text_node.url,
                                       "alt":text_node.text})
    raise Exception("invalid type")
