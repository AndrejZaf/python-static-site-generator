import unittest

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestUtils(unittest.TestCase):
    def test(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        print(new_nodes)

if __name__ == "__main__":
    unittest.main()
