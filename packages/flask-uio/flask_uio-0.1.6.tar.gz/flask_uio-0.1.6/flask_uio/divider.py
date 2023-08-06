from .element import Element

class Divider(Element):
    """Divider widget

    Args:
    
        label (string, optional): divider's label. Defaults to None.
        
    Defaults:
    
        class='ui divider'
    """
    
    def __init__(self, label=None, **attrs):
        super().__init__('div', label, **attrs)
        self.css_class = self.attrs.get('_class') or f'ui divider'
        
        