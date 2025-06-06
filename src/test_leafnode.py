import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "test")
        self.assertEqual(node.to_html(), "<p>test</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test(self):
        LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
