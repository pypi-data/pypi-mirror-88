from .element import Element
from .prop import ValidProp
from .mixin import ReqInjectScriptMixin

class Dropdown(Element, ReqInjectScriptMixin):
    """Dropdown widget 

    Args:
    
        title (string): dropdown's title
        
    Defaults:

        class='ui dropdown'
    
    """
    
    title = ValidProp(str)
    
    def __init__(self, title, *dropdown_menus, **attrs):
        super().__init__('div', hide_id=False, **attrs)
        self.title = title
        self.css_class = self.attrs.get('_class') or f'ui dropdown'
        self.append(Element('div', inner_text=title, _class='text'))
        self.append(Element('i', _class='dropdown icon'))
        self.append(*dropdown_menus)
        self.inject_script = f'load_dropdown("{self.id}", {{on: "hover"}});'
        
class DropdownMenu(Element):
    """Dropdown menu widget
    
    Defaults:
    
        class='menu'
    """
    def __init__(self, *dropdown_menu_items, **attrs):
        super().__init__('div', **attrs)
        self.append(*dropdown_menu_items)
        self.css_class = self.attrs.get('_class') or 'menu'
        
class DropdownMenuItem(Element):
    """Dropdown menu item

    Args:
    
        name (string): item's name
        url (string, optional): link url. Defaults to None.
        icon (Element, optional): item's icon. Defaults to None.
        desc (string, optional): item's description. Defaults to None.
        
    Defaults:
    
        class='item'
    """
    name = ValidProp(str)
    url = ValidProp(str)
    icon = ValidProp(Element)
    desc = ValidProp(str)
    
    def __init__(self, name, url=None, icon=None, desc=None, **attrs):
        
        super().__init__('div', **attrs)
        self.inner_text = name
        
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs.update({'href': self.url})
        
        self.icon = icon
        if self.icon:
            self.append(icon)
            
        self.desc = desc
        if self.desc:
            self.append(Element('span', inner_text=self.desc, _class='description'))
            
        self.css_class = self.attrs.get('_class') or f'item'
        