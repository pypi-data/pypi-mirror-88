from .element import Element, CoreElement
from .mixin import ReqInjectScriptMixin
from .prop import ValidProp, ValidSequenceProp
from .icon import Icon
from .button import Button
from .form import Form

class MessageModal(Element, ReqInjectScriptMixin):
    """Message modal widget

    Args:
    
        title (string): modal's title
        content_elements (list[Element], optional): modal's content. Defaults to None.
        action_elements (list[Element], optional): modal's action button. Defaults to None.
        icon (Icon, optional): modal's icon. Defaults to None.
        scroll_content (bool, optional): enable scroll content. Defaults to False.
        calling_id (string, optional): id of element that is clicked to open the modal. Defaults to None.
        
    More Info:
    
        - See https://fomantic-ui.com/modules/modal.html
    """
    
    title = ValidProp(str)
    content_elements = ValidSequenceProp(CoreElement)
    action_elements = ValidSequenceProp(CoreElement)
    scroll_content = ValidProp(bool)
    icon = ValidProp(Icon)
    calling_id = ValidProp(str)
    
    def __init__(self, title, content_elements=None, action_elements=None, icon=None, scroll_content=False, calling_id=None, **attrs):
    
        super().__init__('div', **attrs)
        self.css_class = self.attrs.get('_class') or 'ui top aligned small modal'
        self.hide_id = False
        self.title = title.title()
        self.content_elements = content_elements
        self.action_elements = action_elements
        self.scroll_content = scroll_content
        self.icon = icon
        self.calling_id = calling_id
            
        header = Element('div', _class='header', inner_text=f'{self.title}')
        if self.icon:
            header.append(self.icon)
        self.append(header)
        
        if self.content_elements:
            css_class = 'scrolling content' if self.scroll_content else 'content'
            content = Element('div', _class=css_class)
            content.append(*tuple(self.content_elements))
            self.append(content)
            
        if self.action_elements:
            actions = Element('div', _class='actions')
            actions.append(*tuple(self.action_elements))
            self.append(actions)
            
        self.inject_script = f'load_modal("{self.calling_id}", "{self.id}");'
        
class ConfirmModal(MessageModal):
    """Confirmation modal widget

    Args:
    
        title (string): modal's title
        message (string): modal's message
        more_message (string, optional): modal's more description. Defaults to None.
        submit_url (string, optional): form's action url. Defaults to None.
        yes (str, optional): customize yes text. Defaults to 'yes'.
        yes_color (str, optional): customzie yes button's color. Defaults to 'red'.
        no (str, optional): customize no text. Defaults to 'no'.
        no_color (str, optional): customzie no button's color. Defaults to 'cancel'.
        icon (Icon, optional): modal's icon. Defaults to None.
        calling_id (string, optional): element's id that is clicked to open the modal. Defaults to None.
        form_id (string, optional): form's id where yes's button submitted to. Defaults to None.
    """
    def __init__(self, title, message, more_message=None, submit_url=None, yes='yes', yes_color='red', no='no', no_color='cancel', icon=None, calling_id=None, form_id=None, **attrs):
        self.message = message
        self.more_message = more_message
        self.submit_url = submit_url
        self.yes_color = yes_color
        self.no_color = no_color
        self.form_id = form_id
        content = Element('p', inner_text=message)
        more_content = Element('', inner_text=more_message)
        yes = Button(yes, _type='submit', _class=f'ui {self.yes_color} button', form_id=self.form_id)
        no = Button(no, _type='button', _class=f'ui {self.no_color} button')
        form = []
        if self.submit_url:
            form.append(Form(action=submit_url).append(yes, no))
        else:
            form.append(Element('div', _class='ui form').append(yes, no))
            
        super().__init__(title, content_elements=[content, more_content], action_elements=form, icon=icon, calling_id=calling_id, **attrs)