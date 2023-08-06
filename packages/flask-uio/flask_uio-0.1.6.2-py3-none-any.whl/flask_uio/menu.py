from .element import Element
from .prop import ValidProp
from .icon import Icon

class Menu(Element):
    
    def __init__(self, *elements, hide_id=True, **attrs):
        super().__init__('div', hide_id=hide_id, **attrs)
        self.css_class = self.attrs.get('_class') or f'ui menu'
        self.append(*elements)
        
class RightMenu(Menu):
    def __init__(self, *elements):
        super().__init__(*elements, _class='right menu')
        
class MenuItem(Element):
    url = ValidProp(str)
    icon = ValidProp(Icon)
    
    def __init__(self, name, url=None, icon=None, hide_id=True, **attrs):
        super().__init__('div', inner_text=name, hide_id=hide_id, **attrs)
        self.url = url
        if self.url is not None:
            self.tag_name = 'a'
        self.icon = icon
        if self.icon:
            self.append(icon)
        self.css_class = self.attrs.get('_class') or 'item'
        if self.url is not None and len(str(self.url).strip()) > 0:
            self.attrs.update({'href': self.url})
        
class MenuHeaderItem(MenuItem):
    def __init__(self, title, url=None, icon=None, **attrs):
        super().__init__(title, url, icon, **attrs)
        self.css_class = self.attrs.get('_class') or 'header item'
        
class MenuActiveItem(MenuItem):
    def __init__(self, title, url=None, icon=None, **attrs):
        super().__init__(title, url, icon, **attrs)
        self.css_class = self.attrs.get('_class') or 'active item'
        
class MenuDisableItem(MenuItem):
    def __init__(self, title, url=None, icon=None, **attrs):
        super().__init__(title, url, icon, **attrs)
        self.css_class = self.attrs.get('_class') or 'disabled item'
        