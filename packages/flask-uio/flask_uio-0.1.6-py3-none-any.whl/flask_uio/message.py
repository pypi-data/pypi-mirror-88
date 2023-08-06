from .segment import Segment
from .prop import ValidProp
from .element import Element
from .icon import Icon

class Message(Element):
    """Message widget

    Args:
    
        message (string): message's text
        opt_css_class (string, optional): option fomantic ui css class. Defaults to None.
        desc (string, optional): message's description. Defaults to None.
        icon (Icon, optional): message's icon. Defaults to None.
        spacing (bool, optional): enable vertical spacing between elements. Defaults to False.
        hideable (bool, optional): auto hide message (10s). Defaults to True.
        
    More Info:
    
        - See https://fomantic-ui.com/collections/message.html
    """
    message = ValidProp(str)
    desc = ValidProp(str)
    opt_css_class = ValidProp(str)
    spacing = ValidProp(bool)
    icon = ValidProp(Icon)
    
    def __init__(self, message, opt_css_class=None, desc=None, icon=None, spacing=False, hideable=True):
        super().__init__('div')
        self.message = message
        self.opt_css_class = ' ' + opt_css_class if opt_css_class else ''
        self.icon = icon
        if icon:
            self.opt_css_class += ' icon'
        self.desc = desc
        self.spacing = spacing
        self.css_class = 'hideable' if hideable else ''
        
        msg_box = Element('div', css_class=f'ui{self.opt_css_class} message')
        if self.icon:
            msg_box.append_inner(self.icon)
        msg_content = Element('div', css_class='content')
        msg_content.append_inner(Element('div', css_class='header', inner_text=self.message))
        if self.desc:
            msg_content.append_inner(Element('p', inner_text=self.desc))
        msg_box.append_inner(msg_content)
        
        if self.spacing:
            segment = Segment(msg_box, opt_css_class='horizontally fitted basic')
            self.append_inner(segment)
        else:
            self.append_inner(msg_box)
            