from .element import Element, CoreElement

class Container(Element):
    """Container widget

    Raises:
    
        ValueError: if element is not an instance of CoreElement.
        
    Defaults:
    
        class='ui container'
    """
    
    def __init__(self, *elements, **attrs):
        super().__init__('div', **attrs)
        for e in elements:
            if not isinstance(e, CoreElement):
                raise ValueError('Invalid elements.')
            self.append(e)
        
        self.css_class = self.attrs.get('_class') or f'ui container'
        