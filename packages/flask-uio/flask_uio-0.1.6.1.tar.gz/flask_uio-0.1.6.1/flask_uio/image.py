from .prop import ValidProp
from .element import Element

class Image(Element):
    """Image widget

    Args:
        src (string): img's src.
        
    More Info:

        - https://fomantic-ui.com/elements/image.html
    """
    src = ValidProp(str)
    
    def __init__(self, src, **attrs):
        super().__init__('img', **attrs)
        self.src = src
        self.attrs.update({'src': self.src})
        self.css_class = self.attrs.get('_class') or f'ui medium image'
        
class LinkImage(Element):
    """Link Image widget

    Args:
        src (string): img's src.
        url (string): link url.
        
    """
    src = ValidProp(str)
    url = ValidProp(str)
    
    def __init__(self, src, url, **attrs):
        super().__init__('a', **attrs)
        self.src = src
        self.url = url
        self.attrs.update({'href': self.url})
        self.append(Element('img', self_closing_tag=True, _src=self.src))
        self.css_class = self.attrs.get('_class') or f'ui medium image'