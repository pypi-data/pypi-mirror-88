from .element import Element
class Text(Element):
    """Text widget

    Args:
        text (string): displayed text
        
    """
    def __init__(self, text, **attrs):
        super().__init__('span', text, **attrs)
        self.css_class = self.attrs.get('_class') or f'ui text'