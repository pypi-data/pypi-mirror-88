from .element import Element
from .divider import Divider
from .prop import ValidProp

class Breadcrumb(Element):
    """Breadcrumb widget

    Args:
        is_dividing (bool, optional): Seperate between sections. Defaults to True.
        
    More Info:
    
        - See https://fomantic-ui.com/collections/breadcrumb.html
    """
    is_dividing = ValidProp(bool)
    
    def __init__(self, is_dividing=True, **attrs):
        
        super().__init__('div', **attrs)
        self.css_class = f'ui breadcrumb'
        self.is_dividing = is_dividing
        if self.is_dividing:
            self.append_next(Divider())

class BreadcrumbSection(Element):
    """Breadcrumb section

    Args:
        title (string): section's title
        url (string, optional): section's url. Defaults to None.
        is_active (bool, optional): apply active style to section. Defaults to False.
    """
    def __init__(self, title, url=None, is_active=False):
        super().__init__('div')
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs.update({'href': self.url})
        self.inner_text = title
        opt = ''
        self.is_active = is_active
        if self.is_active:
            opt = 'active '
        self.css_class = f'{opt}section'
        
class BreadcrumbDividerIcon(Element):
    """Breadcrumb divider icon

    Args:
        icon_css_class (string, optional): fomantic-ui icon class. Defaults to 'right chevron icon divider'.
        
    """
    def __init__(self, icon_css_class=None):
        super().__init__('i')
        self.css_class = icon_css_class + ' divider' if icon_css_class else 'right chevron icon divider'
        
        