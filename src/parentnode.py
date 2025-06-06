from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("Children is missing")
        elements = []
        for child in self.children:
            elements.append(child.to_html())
        elements_str = "".join(elements)
        return f"<{self.tag}>{elements_str}</{self.tag}>"
