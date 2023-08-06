from .element import Element, CoreElement
from .prop import ValidProp

class Segment(Element):
    """Segment widget"""
    def __init__(self, *elements, **attrs):
        super().__init__('div', **attrs)
        for e in elements:
            if not isinstance(e, CoreElement):
                raise ValueError('Element must be an instance of CoreElement.')
            self.append(e)
        if self.css_class is None:
            self.css_class = f'ui segment'
        
class Segments(Element):
    """Segments widget for grouping segments"""
    def __init__(self, *segments, **attrs):
        super().__init__('div', **attrs)
        for e in segments:
            if not isinstance(e, Segment):
                raise ValueError('The object must be an instance of Segment.')
            self.append(e)
        if self.css_class is None:
            self.css_class = f'ui segments'
        