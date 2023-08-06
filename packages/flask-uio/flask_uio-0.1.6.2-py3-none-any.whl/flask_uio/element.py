from .core import CoreElement
from .prop import ValidProp, ValidSequenceProp
from .validator import Validator, Error, RequiredValidator
from .mixin import ReqInjectScriptMixin
from flask import request

class Element(CoreElement):
    """Element is the core of FlaskUIO, it is basically to build an HTML element/tag string.

    Args:
    
        tag_name (string): html tag name.
        inner_text (string, optional): element's inner text. Defaults to None.
        hide_id (bool, optional): hide id attribute. Defaults to True.
        self_closing_tag (bool, optional): open-close tags or single tag. Defaults to False.
        **attrs : html's attribute, use "_" following by attribute's name.
            Example: _class='container', _style='color: red;'
        
    """
    
    tag_name = ValidProp(str)
    css_class = ValidProp(str)
    inner_text = ValidProp(str)
    hide_id = ValidProp(bool)
    self_closing_tag = ValidProp(bool)
    _inner_elements = ValidSequenceProp(CoreElement)
    _prev_elements = ValidSequenceProp(CoreElement)
    _next_elements = ValidSequenceProp(CoreElement)
    
    def __init__(self, tag_name, inner_text=None, hide_id=True, self_closing_tag=False, **attrs):
        
        
        super().__init__(tag_name)
        self.tag_name = tag_name
        self.hide_id = hide_id
        self.attrs = attrs
        self.css_class = self.attrs.get('_class')
        self.inner_text = inner_text
        self.self_closing_tag = self_closing_tag
        setattr(self, '_inner_elements', []) 
        setattr(self, '_prev_elements', []) 
        setattr(self, '_next_elements', []) 
    
    def get_html(self):
        """Generate html string

        Returns: string
        """
        
        # inner text
        inner_text = self.inner_text if self.inner_text else ''
        
        # attributes
        attrs = self._get_string_attrs(**self.attrs)
            
        # inner_elements
        inner_element_html = ''
        if self._inner_elements:
            for obj in self._inner_elements:
                inner_element_html += obj.get_html()
                
        # prev_elements
        prev_element_html = ''
        if self._prev_elements:
            for obj in self._prev_elements:
                prev_element_html += obj.get_html()
                
        # next_elements
        next_element_html = ''
        if self._next_elements:
            for obj in self._next_elements:
                next_element_html += obj.get_html()  
                
        # css class
        css_class = ''
        if self.css_class:
            css_class = f' class="{self.css_class}"'
                
        # tag id
        tag_id = '' if self.hide_id else f' id="{self.id}"'
        
        if self.tag_name == '':
            html = f'{inner_text}{inner_element_html}'
        else:
            if self.self_closing_tag:
                html = f'<{self.tag_name}{tag_id}{css_class}{attrs} />'
            else:
                html = f'<{self.tag_name}{tag_id}{css_class}{attrs}>{inner_element_html}{inner_text}</{self.tag_name}>'
        
        return prev_element_html + html + next_element_html
        
    def append(self, *elements):
        """Append inner elements

        Returns: self
        """
        if not hasattr(self, '_inner_elements'):
            setattr(self, '_inner_elements', [])
        
        for element in elements:
            self._append_element(self, '_inner_elements', element)
        return self
    
    def append_prev(self, *elements):
        for element in elements:
            self._append_element(self, '_prev_elements', element)
        return self
        
    def append_next(self, *elements):
        for element in elements:
            self._append_element(self, '_next_elements', element)   
        return self     
    
    def find_element(self, *types):
        """Find inner element by type

        Returns: list[Element]
        """
        
        result = []
        if self._inner_elements:
            for obj in self._inner_elements:
                if isinstance(obj, types):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(types)
                        if len(finding) > 0:
                            result += finding
                            
        if self._prev_elements:
            for obj in self._prev_elements:
                if isinstance(obj, types):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(types)
                        if len(finding) > 0:
                            result += finding
        if self._next_elements:
            for obj in self._next_elements:
                if isinstance(obj, types):
                    result += [obj]
                else:
                    if hasattr(obj, 'find_element'):
                        finding = obj.find_element(types)
                        if len(finding) > 0:
                            result += finding
        
        return result
            
class Link(Element):
    """Link widget for building html link element

    Args:
        href (str, optional): url path. Defaults to 'index.css'.
    """
    href = ValidProp(str)
    
    def __init__(self, href='index.css'):
        self.href = href
        super().__init__('link', self_closing_tag=True, _rel='stylesheet', _type='text/css', _href=self.href)
        
class Script(Element):
    """Script widget for building html script element

    Args:
        src (str, optional): url path. Defaults to 'index.js'.
    """
    src = ValidProp(str)
    
    def __init__(self, src='index.js'):
        self.src = src
        super().__init__('script', _src=self.src)
        
class Head(CoreElement):
    """Head widget for building html head element.

    Args:
        title (string): Page's title
        elements (list[Element], optional): list of element. Defaults to None.
        links (list[Link], optional): list of link. Defaults to None.
        scripts (list[Script], optional): list of script. Defaults to None.
    """
    title = ValidProp(str, nullable=False)
    _elements = ValidSequenceProp(CoreElement)
    _links = ValidSequenceProp(CoreElement)
    _scripts = ValidSequenceProp(CoreElement)
    
    def __init__(self, title, elements=None, links=None, scripts=None, **attrs):
        
        super().__init__('head')
        self.title = title
        self._elements = elements
        self._links = links
        self._scripts = scripts
        self.attrs = attrs
        self.append(Element('title', inner_text=title))
        self.append(Element('meta', _charset='UTF-8'))
        self.append(Element('meta', _name='viewport', _content='width=device-width, initial-scale=1.0'))
    
    def append(self, *elements):
        """Append inner elements"""
        for element in elements:
            self._append_element(self, '_elements', element)
        
    def append_link(self, *hrefs):
        """Append link"""
        for href in hrefs:
            if not isinstance(href, str):
                raise ValueError('href must be a string.')
            link = Link(href)
            self._append_element(self, '_links', link)
        
    def append_script(self, *srcs):
        """Append script"""
        for src in srcs:
            if not isinstance(src, str):
                raise ValueError('src must be a string.')
            self._append_element(self, '_scripts', Script(src))

    def get_html(self):
        """Generate html string

        Returns: string
        """
        html = ''
        fields = ['_elements', '_links', '_scripts']
        for field in fields:
            elements = getattr(self, field)
            for obj in elements:
                html += obj.get_html()
        
        # exclude _class 
        attrs = self._get_string_attrs(**self.attrs)
        
        return f'<{self.tag_name}{attrs}>{html}</{self.tag_name}>'
class Body(CoreElement):
    '''Body widget for building html body element.
    
    Args:
        elements (list[Element], optional): list of element. Defaults to None.
        scripts (list[Script], optional): list of script. Defaults to None.
        injected_scripts (list[Script], optional): list of script that will be injected later. Defaults to None.
    
    '''
    
    _elements = ValidSequenceProp(CoreElement)
    _scripts = ValidSequenceProp(Script)
    _injected_scripts = ValidSequenceProp(Script)
    
    def __init__(self, elements=None, scripts=None, injected_scripts=None, **attrs):
        super().__init__('body')
        self._elements = elements
        self._scripts = scripts
        self._injected_scripts = injected_scripts
        self.attrs = attrs
        self.css_class = self.attrs.get('_class')
    
    def append(self, *elements):
        """Append elements to body"""
        
        for element in elements:
            self._append_element(self, '_elements', element)
        
    def append_script(self, *srcs):
        """Append scripts to body"""
        
        for src in srcs:
            if not isinstance(src, str):
                raise ValueError('Each src must be a string.')
            self._append_element(self, '_scripts', Script(src))
            
    def append_injected_script(self, *scripts):
        """Append injected scripts to body"""
        
        for element in scripts:
            self._append_element(self, '_injected_scripts', element)

    def get_html(self):
        """Generate html string
        
        Return: string
        """
        
        html = ''
        injected_script = ''
        fields = ['_elements', '_scripts']
        for field in fields:
            for obj in getattr(self, field):
                html += obj.get_html()
        
        inject_elements = []
        for obj in getattr(self, '_elements'):
            if isinstance(obj, ReqInjectScriptMixin):
                script = Element('script', inner_text=obj.inject_script)
                self.append_injected_script(script)
            
            if isinstance(obj, Element):
                inject_elements += obj.find_element(ReqInjectScriptMixin)
                for field in inject_elements:
                    script = Element('script', inner_text=field.inject_script)
                    self.append_injected_script(script)
        
        # Check for injected script
        if len(self._injected_scripts) > 0:
            for script in self._injected_scripts:
                injected_script += script.get_html()
                
        # exclude _class
        attrs = self._get_string_attrs(**self.attrs)
        
        # independent attr for sub-class customization
        css_class = ''
        if self.css_class:
            css_class = f' class="{self.css_class}"'
        
        return f'<{self.tag_name}{css_class}{attrs}>{html}{injected_script}</{self.tag_name}>'

class Html():
    """Html widget for building html element.

    Args:
        title (string): Page's title
        
    """
    def __init__(self, title):
        self.head = Head(title)
        self.body = Body()
    
    def get_html(self):
        doctype = '<!DOCTYPE html>'
        html = Element('html', _lang='en')
        head_html = self.head.get_html()
        body_html = self.body.get_html()
        html.inner_text = head_html + body_html
        return doctype + html.get_html()

class FieldElement(Element):
    """Field element is used for providing functionality to form field.

    Args:
    
        tag_name (string): html tag name.
        id (string, optional): set custom id html attribute. Defaults to None.
        name (string, optional): set name html attribute. Defaults to None.
        placeholder (string, optional): set placeholder. Defaults to None.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        required (bool, optional): set required attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
        validators (list[Validator], optional): add validators (auto add RequiredValidator if required). Defaults to None.
    """
    id = ValidProp(str)
    name = ValidProp(str)
    placeholder = ValidProp(str)
    disabled = ValidProp(bool)
    required = ValidProp(bool)
    readonly = ValidProp(bool)
    error = ValidProp(Error)
    validators = ValidSequenceProp(Validator)
    
    def __init__(self, tag_name, id=None, name=None, placeholder=None, disabled=False, required=False, readonly=False, validators=None, **attrs):
        
        super().__init__(tag_name, hide_id=False, **attrs)
        
        self.id = id if id else self.id
        self.name = name.replace('_', ' ').title()
        self.placeholder = placeholder if placeholder else self.name
        self.disabled = disabled
        self.readonly = readonly
        self.error = Error(False)
        self.required = required
        
        self.validators = []
        if self.required:
            self.validators.append(RequiredValidator())
        
        if validators:
            self.validators = self.validators + validators
        
        opt_attrs = {}
        
        if self.name:
            opt_attrs.update({'_name': self.name})
            
        if self.placeholder:
            opt_attrs.update({'_placeholder': self.placeholder})
            
        if self.readonly:
            opt_attrs.update({'_readonly': True})
            
        if self.disabled:
            opt_attrs.update({'_disabled': True})
        
        self.attrs.update(opt_attrs)
        self._data = None
            
    @property
    def form_data(self):
        """Request form data

        Returns:
            data: request form data
        """
        is_multiple = getattr(self, 'is_multiple', None)
        if is_multiple:
            data = request.form.getlist(self.name)
        data = request.form.get(self.name, None)
        if data:
            return data
        else:
            return self._data
    
    @property
    def data(self):
        """Override depend on field data type"""
        pass
    
    @data.setter
    def data(self, value):
        """Override depend on field data type"""
        pass
    
    def validate(self):
        """Validate form data

        Raises:
            Exception: if not an instance of Validator.

        Returns:
            Error: status and message.
        """
        if request.method in ('PUT', 'POST', 'DELETE'):
            for v in self.validators:
                if not isinstance(v, Validator):
                    raise Exception('validator must be an instance of Validator.')
                self.error = v.validate(self.name, self.form_data)
                if self.error.status:
                    break
            return self.error