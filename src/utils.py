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
    old_nodes
