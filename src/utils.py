from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode, TextType
import re
from enum import Enum

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
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL_TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL_TEXT)
    initial_split = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
    secondary_split = split_nodes_delimiter(initial_split, "_", TextType.ITALIC_TEXT)
    third_split = split_nodes_delimiter(secondary_split, "`", TextType.CODE_TEXT)
    fourth_split = split_nodes_image(third_split)
    fifth_split = split_nodes_link(fourth_split)
    return fifth_split
   
def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    stripped_markdown = list(map(str.strip, markdown_split))
    filtered_markdown = list(filter(None, stripped_markdown))
    return filtered_markdown

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(">"):
        result = check_each_line(block, ">")
        return BlockType.QUOTE if result is None else BlockType.PARAGRAPH
    elif block.startswith("- "):
        result = check_each_line(block, "- ")
        return BlockType.UNORDERED_LIST if result is None else BlockType.PARAGRAPH
    elif block.startswith("#") and check_valid_heading(block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
       return BlockType.CODE
    elif block[0] == "1" and check_valid_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def check_each_line(block, sequence):
    lines = block.split("\n")
    for line in lines:
        if line.startswith(sequence):
            continue
        else:
            return BlockType.PARAGRAPH
    return None


def check_valid_heading(block):
    count = 0
    for character in block:
        if character == "#" and count <= 6:
            count += 1
            continue
        elif character == " " and count <= 6:
            break
        else:
            return False
    return True if len(block) > count + 1 else False

def check_valid_ordered_list(block):
    rows = block.split("\n")
    for index in range(len(rows)):
        if rows[index][0] == str(index + 1) and rows[index][1] == "." and rows[index][2] == " " and len(rows[index]) > 3:
            continue
        else:
            return False
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        text_nodes = text_to_textnodes(block)
        html_text_nodes = list(map(text_node_to_html_node, text_nodes))
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(HTMLNode("p", "", html_text_nodes))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(HTMLNode("blockquote", "", html_text_nodes))
        elif block_type == BlockType.CODE:
            lines = block.split("\n")[1:-1]
            html_nodes.append(HTMLNode("pre", "", [HTMLNode("code", "\n".join(lines))]))
        elif block_type == BlockType.HEADING:
            blocks_split = block.split(" ", 1)
            heading_text_nodes = text_to_textnodes(blocks_split[1])
            html_nodes.append(HTMLNode(f"h{len(blocks_split[0])}", "", heading_text_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            pass
        elif block_type == BlockType.ORDERED_LIST:
            pass
    return HTMLNode("div", "", html_nodes)

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
print(markdown_to_html_node(md))
