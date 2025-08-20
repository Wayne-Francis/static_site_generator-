
class HTMLNode():

    def __init__(self,tag = None, value = None ,children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        if not self.props:
            return ""
        message = ""
        for prop in self.props:
            message += f' {prop}="{self.props[prop]}"'
        return message 

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if self.tag == None:
            return f"{self.value}" 
        prop_message = ""
        if self.props == None:
            prop_message = ""
        if not self.props:
            prop_message = ""
        if self.props:
            for prop in self.props:
                prop_message += f' {prop}="{self.props[prop]}"'
        return f'<{self.tag}{prop_message}>{self.value}</{self.tag}>'
