from .element import Element
from .prop import ValidProp, IntProp
from .func import get_word

class Grid(Element):
    nb_col = IntProp(1,16)
    
    def __init__(self, *elements, nb_col=None, **attrs):
        super().__init__('div', **attrs)
        self.nb_col = nb_col
        
        opt = ''
        if self.nb_col:
            opt = ' ' + get_word(self.nb_col) + ' column'
                
        self.css_class = self.attrs.get('_class') or f'ui{opt} grid'
        self.append(*elements)
        
class GridColumn(Element):
    nb_wide = IntProp(1,16)
    
    def __init__(self, *elements, nb_wide=None, **attrs):
        super().__init__('div', **attrs)
        self.nb_wide = nb_wide
        opt = ''
        if self.nb_wide:
            opt = get_word(nb_wide) + ' wide '
        self.css_class = self.attrs.get('_class') or f'{opt}column'
        self.append(*elements)
        
class GridRow(Element):
    nb_col = IntProp(1,16)
    
    def __init__(self, *elements, nb_col=None, **attrs):
        super().__init__('div', **attrs)
        self.nb_col = nb_col
        opt = ''
        if self.nb_col:
            opt = get_word(nb_col) + ' column '
        self.css_class = self.attrs.get('_class') or f'{opt}row'
        self.append(*elements)