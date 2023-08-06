from .element import Element, FieldElement
from .prop import ValidProp
from flask import request, flash
from flask_wtf.csrf import generate_csrf
class Form(Element):
    """Form widget

    Args:
    
        method (str, optional): form's method. Defaults to 'POST'.
        action (string, optional): form's action. Defaults to None.
        has_file (bool, optional): required for fileupload. Defaults to None.
    """
    method = ValidProp(str)
    action = ValidProp(str)
    has_file = ValidProp(bool)
    
    def __init__(self, method='POST', action=None, has_file=None, **attrs):
        super().__init__('form', hide_id=False, **attrs)
        self.method = method
        self.append(self.create_csrf_field())
        self.has_file = has_file
        
        if self.method and self.method.upper() in ('GET', 'POST', 'PUT', 'DELETE'):
            self.attrs.update({'method': self.method})
        
        if self.attrs:
            self.attrs.update({'action': action})
            
        if self.has_file:
            self.attrs.update({'enctype': 'multipart/form-data'})
        
        self.css_class = self.attrs.get('_class') or f'ui form'
        self.errors = []
        
    @staticmethod
    def create_csrf_field():
        return Element('input', _type='hidden', _name='csrf_token', _value=generate_csrf())
    
    def validate_on_submit(self):
        if request.method in ('PUT', 'POST', 'DELETE'):
            errors = []
            for _, f in self.__dict__.items():
                if isinstance(f, FieldElement) and f.validate():
                    errors.append(f.validate())
            self.errors = errors
            return len([e for e in self.errors if e.status]) == 0
        
    def render(self):
        raise NotImplementedError()
    
    @staticmethod
    def flash_success(message='Success', category='success'):
        flash(message, category)
    
    @staticmethod
    def flash_error(message='Fail', category='error'):
        flash(message, category)