import unittest

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType

class TestUtils(unittest.TestCase):
    def test(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL_TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            )], new_nodes)

    def test_split_images2(self):
        node = TextNode("This is before ![first](url1) middle ![second](url2) after.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is before ", TextType.NORMAL_TEXT),
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.NORMAL_TEXT),
            TextNode("second", TextType.IMAGE, "url2"),
            TextNode(" after.", TextType.NORMAL_TEXT)], new_nodes)

    def test_split_images3(self):
        node = TextNode("![start](img1) then some text ![middle](img2) end.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("start", TextType.IMAGE, "img1"),
            TextNode(" then some text ", TextType.NORMAL_TEXT),
            TextNode("middle", TextType.IMAGE, "img2"),
            TextNode(" end.", TextType.NORMAL_TEXT)], new_nodes)

    def test_split_images4(self):
        node = TextNode("start ![one](url1) mid ![two](url2) end", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("start ", TextType.NORMAL_TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" mid ", TextType.NORMAL_TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.NORMAL_TEXT)], new_nodes)

    def test_split_images5(self):
        node = TextNode("before ![a](urlA)![b](urlB) after", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("before ", TextType.NORMAL_TEXT),
            TextNode("a", TextType.IMAGE, "urlA"),
            TextNode("b", TextType.IMAGE, "urlB"),
            TextNode(" after", TextType.NORMAL_TEXT)], new_nodes)

    def test_split_links(self):
        node = TextNode("[Boot.dev](https://www.boot.dev) is a great learning platform.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is a great learning platform.", TextType.NORMAL_TEXT)], new_nodes)

    def test_combined_functions(self):
        new_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(new_text)
        print(nodes, "count", len(nodes))
        self.assertListEqual([
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")], nodes)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"])



    def test_block_to_block_type(self):
        test = ">test\n>test2"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockType.QUOTE)

        
if __name__ == "__main__":
    unittest.main()
