from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from block import BlockType, block_to_block_type
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        end_reached = False
        tmp_nodes = []
        i = 0
        j = 0
        while(not end_reached):
            i = old_node.text.find(delimiter, j)
            if i == -1:
                tmp_nodes.append(TextNode(old_node.text[j:], TextType.TEXT))
                break
            if i != j:
                tmp = old_node.text[j:i]
                tmp_nodes.append(TextNode(tmp, TextType.TEXT))
            j = old_node.text.find(delimiter, i + len(delimiter))
            if j == -1:
                raise Exception("one " + delimiter + " is missing")
            tmp = old_node.text[i+len(delimiter):j]
            tmp_nodes.append(TextNode(tmp, text_type))
            j += len(delimiter)
            if j >= len(old_node.text) - 1:
                end_reached = True
        new_nodes.extend(tmp_nodes)
    return new_nodes

def extract_markdown_images(text):
    imgs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return imgs

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            nodes.append(node)
            continue
        tmp_section = node.text
        for image in images:
            section = tmp_section.split(f"![{image[0]}]({image[1]})", 1)
            tmp_section = section[1]
            if section[0] != "":
                nodes.append(TextNode(section[0], TextType.TEXT))
            nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        if tmp_section != "":
            nodes.append(TextNode(tmp_section, TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            nodes.append(node)
            continue
        tmp_section = node.text
        for link in links:
            section = tmp_section.split(f"[{link[0]}]({link[1]})", 1)
            tmp_section = section[1]
            if section[0] != "":
                nodes.append(TextNode(section[0], TextType.TEXT))
            nodes.append(TextNode(link[0], TextType.LINK, link[1]))
    return nodes

def text_to_textnodes(text):
    initial_textnode = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([initial_textnode], '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        match(block_to_block_type(block)):
            case(BlockType.PARAGRAPH):
                children.append(paragraph_to_html_node(block))
            case(BlockType.CODE):
                children.append(code_to_html_node(block))
            case(BlockType.HEADING):
                children.append(heading_to_html_node(block))
            case(BlockType.QUOTE):
                children.append(quote_to_html_node(block))
            case(BlockType.UNORDERED_LIST):
                children.append(unordered_to_html_node(block))
            case(BlockType.ORDERED_LIST):
                children.append(ordered_to_html_node(block))

    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level > 6:
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    raw_text = block[4:-3]
    textnode = TextNode(raw_text, TextType.TEXT)
    child = text_node_to_html_node(textnode)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        line = line[2:]
        new_lines.append(line)
    paragraph = " ".join(new_lines)
    children = text_to_children(paragraph)
    return ParentNode("blockquote", children)

def unordered_to_html_node(block):
    lines = block.split("\n")
    li = []
    for line in lines:
        line = line[2:]
        li.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", li)

def ordered_to_html_node(block):
    lines = block.split("\n")
    li = []
    for line in lines:
        new_line = re.findall(r"^\d+\.\ (.*?)$", line)[0]
        li.append(ParentNode("li", text_to_children(new_line)))
    return ParentNode("ol", li)
