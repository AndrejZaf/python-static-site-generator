from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Invalid type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)

        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Missing closing delimiter")

        nodes = node.text.split(delimiter)
        for index in range(len(nodes)):
            if index % 2 != 0:
                new_nodes.append(TextNode(nodes[index], text_type))
            else:
                new_nodes.append(TextNode(nodes[index], TextType.NORMAL_TEXT))
                
    return new_nodes

