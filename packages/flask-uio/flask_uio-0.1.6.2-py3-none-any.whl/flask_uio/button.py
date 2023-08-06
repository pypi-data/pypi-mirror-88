from .element import Element
from .prop import ValidProp

class Button(Element):
    """Button widget
    
    Args:
    
        title (str): button's title. 
        form_id (str): id of form to be submitted.
    
    Defaults: 
    
        attrs:
            type='submit'
            class='ui button'
    """
    title = ValidProp(str)
    form_id = ValidProp(str)
    
    def __init__(self, title, form_id=None, **attrs):
        super().__init__('input', hide_id=False, **attrs)
        self.title = title
        self.form_id = form_id
        
        self.attrs.update({
            'type': 'submit',
            'value': self.title.title()
        })
            
        if self.form_id:
            self.attrs.update({'form': self.form_id})
        
        self.css_class = self.attrs.get('_class') or 'ui button'
        
class LinkButton(Element):
    """Link button widget
    
    Args:
    
        title (str): button's title. 
        url (str): linked url. 
        attrs : element's attributes.
    
    Defaults: 
    
        attrs:
            class='ui button'
        
    """
    url = ValidProp(str)
    
    def __init__(self, title, url, **attrs):
        super().__init__('a', inner_text=title, **attrs)
        self.url = url
        self.attrs.update({'href': self.url})
        self.css_class = self.attrs.get('_class') or 'ui button'
        