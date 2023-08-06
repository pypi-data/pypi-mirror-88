from .element import Element
from .prop import ValidProp

class Icon(Element):
    """Icon widget
    
    Args:
        
        css_class (str): set icon css class.
    """
    def __init__(self, css_class):
        super().__init__('i', _class=css_class)
        
class LinkIcon(Element):
    """LinkIcon widget
    
    Args:
        
        css_class (str): set icon css class.
        url (str): url.
        target (str, optional): '_self', '_blank', '_parent', '_top'
        
    More Info:
    
        - See https://fomantic-ui.com/elements/icon.html
    """
    
    url = ValidProp(str)
    target = ValidProp(str)
    def __init__(self, css_class, url, target=None):
        super().__init__('a', _class=css_class)
        self.url = url
        self.target = target
        self.attrs.update({'href': self.url})
        if self.target:
            self.attrs.update({'target': self.target})
        self.append(Icon(css_class))