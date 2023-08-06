from .element import Element, FieldElement
from .mixin import ReqInjectScriptMixin
from .prop import ValidProp, ValidSequenceProp
from .token import Token
from .validator import UploadValidator
from flask import current_app, url_for, request
from datetime import date, datetime
from werkzeug.utils import secure_filename
import os
import requests

class Field(Element):
    """Field widget for styling control with fomantic-ui.

    Args:
        required (bool, optional): apply required style. Defaults to False.
        error (bool, optional): apply error style. Defaults to False.
        disabled (bool, optional): apply disabled style. Defaults to False.
        css_class (string, optional): apply custom style. Defaults to None.
        
    """
    def __init__(self, *elements, required=False, error=False, disabled=False, css_class=None):
        super().__init__('div')
        required_field = 'required ' if required else ''
        error_field = ' error' if error else ''
        disabled_field = ' disabled' if disabled else ''
        default_css = 'field'
        css_class = css_class if css_class else default_css
        self.css_class = f'{required_field}{css_class}{error_field}{disabled_field}'
        self.append(*elements)

class CheckBoxField(FieldElement, ReqInjectScriptMixin):
    """Checkbox field widget 

    Args:
        name (string): input's name.
        disabled (bool, optional): apply disabled style. Defaults to False.
        readonly (bool, optional): apply readonly attribute to input. Defaults to False.
        **attrs : html attributes.
    """
    _value = ValidProp(bool)
    
    def __init__(self, name, disabled=False, readonly=False, **attrs):
        super().__init__('', name=name, disabled=disabled, readonly=readonly, required=False)
        # input
        self._input_attrs = {
            'type': 'checkbox',
            'tabindex': '0',
            'class': 'hidden',
        }
        self._input_attrs.update(attrs)
        self.input = Element('input', **self._input_attrs)
        
        # input wrapper
        wrapper = Element('div', hide_id=False, _class='ui checkbox')
        wrapper.append(
            self.input, 
            Element('label', inner_text=self.name.replace('_', ' ').title())
        )
        
        # field validation
        self.validate()
        
        # field wrapper 
        field_wrapper = Field(wrapper, required=self.required, disabled=self.disabled, error=self.error.status, css_class='inline field')
        
        self.append(field_wrapper)
        self.inject_script = f'load_checkbox_field("{wrapper.id}");'
        
    @property
    def data(self):
        return True if self.form_data else False
        
    @data.setter
    def data(self, value):
        if value:
            self.input.attrs.update({'checked': True})
            self._data = value

class DateField(FieldElement, ReqInjectScriptMixin):
    """Date field widget

    Args:
        name (string): input's name
        required (bool, optional): set required attribute. Defaults to False.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
        placeholder (string, optional): set placeholder. Defaults to None.
        validators (list[Validator], optional): add validators (auto add RequiredValidator if required). Defaults to None.
        
    """
    def __init__(self, name, required=False, disabled=False, readonly=False, placeholder=None, validators=None):
        
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required, validators=validators)
        self.py_format = current_app.config['FLASK_UIO_DATE_DISPLAY_FORMAT']
        self.js_format = current_app.config['FLASK_UIO_DATE_JS_FORMAT']
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        
        self.attrs.update({'type': 'text', 'autocomplete': 'off'})
        self.input = Element('input', **self.attrs)
        self.input_wrapper = Element('div', hide_id=False, _class='ui calendar')
        self.input_wrapper.append(
            Element('div', _class='ui input').append(self.input)
        )
        
        # validate
        self.validate()
        
        # ui
        wrapper = Field(label, self.input_wrapper, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.status:
            wrapper.append(Element('div', self.error.message, _class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
        self.inject_script = f'load_date_field("{self.input_wrapper.id}", "{self.js_format}");'

    @property
    def data(self):
        try:
            return datetime.strptime(self.form_data, self.py_format).date() if self.form_data else self.form_data
        except Exception:
            return None
        
    @data.setter
    def data(self, value):
        if value and not isinstance(value, (date, datetime)):
            raise ValueError(f'{self.name} must be a date/datetime.')
        # reset ui
        fm_date = datetime.strftime(value, self.py_format) if value else self.form_data
        self.input.attrs.update({'value': fm_date})
        self._data = value
        
class DateTimeField(FieldElement, ReqInjectScriptMixin):
    """DateTime field widget

    Args:
        name (string): input's name
        required (bool, optional): set required attribute. Defaults to False.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
        placeholder (string, optional): set placeholder. Defaults to None.
        validators (list[Validator], optional): add validators (auto add RequiredValidator if required). Defaults to None.
        
    """
    def __init__(self, name, required=False, disabled=False, readonly=False, placeholder=None, validators=None):
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required, validators=validators)
        self.py_format = current_app.config['FLASK_UIO_DATETIME_DISPLAY_FORMAT']
        self.js_format = current_app.config['FLASK_UIO_DATETIME_JS_FORMAT']
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        
        self.attrs.update({'type': 'text', 'autocomplete': 'off'})
        self.input = Element('input', **self.attrs)
        self.input_wrapper = Element('div', hide_id=False, _class='ui calendar')
        self.input_wrapper.append(
            Element('div', _class='ui input').append(self.input)
        )
        
        # validate
        self.validate()
        
        # ui
        wrapper = Field(label, self.input_wrapper, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.status:
            wrapper.append(Element('div', self.error.message, _class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
                          
        self.inject_script = f'load_datetime_field("{self.input_wrapper.id}", "{self.js_format}");'
            
    @property
    def data(self):
        try:
            return datetime.strptime(self.form_data, self.py_format) if self.form_data else self.form_data
        except Exception:
            return None
        
    @data.setter
    def data(self, value):
        if value and not isinstance(value, (date, datetime)):
            raise ValueError(f'{self.name} must be a date/datetime.')
        # reset ui
        fm_date = datetime.strftime(value, self.py_format) if value else self.form_data
        self.input.attrs.update({'value': fm_date})
        self._data = value

class DropDownField(FieldElement, ReqInjectScriptMixin):
    """Dropdown field widget

    Args:
    
        name (string): input's name
        choices (:obj:`list` of :obj:`tuple`, optional): key-value tuple list. Defaults to None.
        required (bool, optional): set required attribute. Defaults to False.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
    """
    inject_script = ValidProp(str)
    choices = ValidSequenceProp(tuple)
    
    def __init__(
            self, 
            name, 
            choices=None,
            required=False, 
            disabled=False, 
            readonly=False,
        ):
        
        super().__init__('', name=name, disabled=disabled, readonly=readonly, required=required)
        
        self.attrs.update({'type': 'text', 'class':'ui search clearable selection dropdown'})
        
        self.choices = [('Select One', '')] + choices
        options = []
        if self.choices:
            for n, v in self.choices:
                options.append(Element('option', inner_text=n, _value=f"{v}"))
        
        # create layout
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        self.input = Element('select', hide_id=False, **self.attrs)
        self.input.append(*tuple(options))
        
        self.validate()
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.message:
            wrapper.append(Element('div', inner_text=self.error.message, _class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
        self.inject_script = f'load_dropdown_field("{self.input.id}");'
           
    @property
    def data(self):
        return self.form_data
        
    @data.setter
    def data(self, value):
        # reset ui
        value = value if value else self.form_data
        self._data = value
        options = []
        if self.choices:
            for n, v in self.choices:
                if value == v:
                    options.append(Element('option', inner_text=n, _value=v, _selected='selected'))
                else:
                    options.append(Element('option', inner_text=n, _value=v))
        self.input._inner_elements = options

class QueryDropDownField(FieldElement, ReqInjectScriptMixin):
    """Query dropdown field widget

    Args:
    
        name (string): field's name.
        required (bool, optional): set required attribute. Defaults to False.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
        dbname (string, optional): database's name (required setup app config). Defaults to None.
        field_id (string, optional): key field's name. Defaults to None.
        field_name (string, optional): value field's name. Defaults to None.
        from_table (string, optional): table's name. Defaults to None.
        where (string, optional): sql query for where. Defaults to None.
        order_by (string, optional): sql query for order by. Defaults to None.
        additional_where (string, optional): sql query for where additionally. Defaults to None.
        fk_field_id (string, optional): field's name for children dropdown query. Defaults to None.
        parents (list[QueryDropDownField], optional): for dependent dropdown. Defaults to None.
    
    Note: 
    
        - Support only flask_sqlalchemy
    
    Setup::
    
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_DATABASE_URI_DICT'] = {
            'test': 'sqlite:///test.db',
        }
        app.config['FLASK_UIO_FERNET_SECRET_KEY'] = 'your_fernet_secret_key'
        # >>> from flask_uio import Token
        # >>> Token.key()
        
    Example::

        category = uio.QueryDropDownField(
            'category',
            True,
            dbname='test',
            field_id='id',
            field_name='name',
            from_table='category',
            order_by='name desc',
        )
        post = uio.QueryDropDownField(
            'post',
            True,
            dbname='test',
            field_id='id',
            field_name='title',
            from_table='post',
            where=f'category_id = {category.data if category.data else 0}',
            parents=[category]
        )
        
    """
    
    dbname = ValidProp(str)
    field_id = ValidProp(str)
    field_name = ValidProp(str)
    from_table = ValidProp(str)
    where = ValidProp(str)
    order_by = ValidProp(str)
    additional_where = ValidProp(str)
    inject_script = ValidProp(str)
    
    parents = []
    
    def __init__(
            self, 
            name, 
            required=False, 
            disabled=False, 
            readonly=False,
            dbname=None, 
            field_id=None, 
            field_name=None, 
            from_table=None, 
            where=None, 
            order_by=None,
            additional_where=None, 
            fk_field_id=None, 
            parents=None
        ):
        
        
        super().__init__('', name=name, disabled=disabled, readonly=readonly, required=required)
        
        self.attrs.update({'type': 'text'})
        self.choices = []
        self.dbname = dbname
        self.field_id = field_id
        self.field_name = field_name
        self.from_table = from_table
        self.where = where
        self.order_by = order_by
        self.additional_where = additional_where
        self.dependents = []
            
        self.fk_field_id = fk_field_id or f'{self.from_table}_{self.field_id}'
        
        self._init_data_source()
        
        options = []
        if self.choices:
            for n, v in self.choices:
                options.append(Element('option', n, _value=v))
        
        # create layout
        label = Element('label', self.name.title(), _for=self.name)
        self.input = Element('select', hide_id=False, _class='ui search clearable selection dropdown', **self.attrs)
        self.input.append(*tuple(options))
        
        self.validate()
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.message:
            wrapper.append(Element('div',self.error.message ,_class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
    
        self._ref_id = self.input.id
        
        if parents:
            self.parents = parents
            
            for p in self.parents:
                p._add_dependent(self)
                
        self.inject_script = f'load_relationship_dropdown_field_ajax("{self.input.id}");'
           
    def _init_data_source(self):
        additional_where = self.additional_where or ''
        where = f'where {self.where} {additional_where}' if self.where else ''
        order_by = f"order by {self.order_by}" if self.order_by else f"order by {self.field_name} asc"
        
        sql = (
            f"select {self.field_id} as id, {self.field_name} as name "
            f"from {self.from_table} "
            f"{where} "
            f"{order_by}"
        )
        
        if self.dbname:
            token = Token(str(current_app.config.get('FLASK_UIO_FERNET_SECRET_KEY')).encode())
            server_name = current_app.config.get('FLASK_UIO_API_SERVER')
            res = requests.get(url=server_name + url_for('flaskuio.query_dropdown', e_db=token.encrypt(self.dbname), e_sql=token.encrypt(sql)))
            if res.status_code != 200:
                raise Exception(res.text)
            for opt in res.json():
                self.choices.append((str(opt['name']), str(opt['id'])))
        
    def _add_dependent(self, *dependents):
        for d in dependents:
            if not isinstance(d, type(self)):
                raise ValueError(f'dependent must be an instance of {type(self).__name__}.')
            self.dependents.append(d)
        
        token = Token(str(current_app.config.get('FLASK_UIO_FERNET_SECRET_KEY')).encode())
        js_obj = []
        refs = []
        for d in self.dependents:
            based_where = ''
            for p in d.parents:
                refs.append(f"'{p._ref_id}'")
                if based_where == '':
                    based_where += f" {p.fk_field_id}={p._ref_id}"
                else:
                    based_where += f" and {p.fk_field_id}={p._ref_id}"
            # prepare query
            where = f'where {based_where}'
            additional_where = d.additional_where or ''
            
            child_sql = (
                f"select {d.field_id} as id, {d.field_name} as name "
                f"from {d.from_table} "
                f"{where} {additional_where} "
                f"order by {d.field_name} asc;"
            )
            
            # encrypt sql and dbname
            e_child_sql = token.encrypt(child_sql)
            e_db = token.encrypt(d.dbname)
            
            # prepare javascript dependent objects
            js_refs = ','.join(refs)
            js_obj.append(f'{{child_ref_id:"{d._ref_id}", child_sql:"{e_child_sql}", child_db:"{e_db}", depend_on:[{js_refs}]}}')
            
        js_list = ','.join(js_obj)
        
        # update script
        self.inject_script = f'load_relationship_dropdown_field_ajax("{self._ref_id}", [{js_list}]);'
        
    @property
    def data(self):
        return self.form_data
        
    @data.setter
    def data(self, value):
        # reset ui
        value = value if value else self.form_data
        self._data = value
        options = []
        if self.choices:
            for n, v in self.choices:
                if value == v:
                    options.append(Element('option', n, _value=v, _selected='selected'))
                else:
                    options.append(Element('option', n, _value=v))
        self.input._inner_elements = options
        
class TextField(FieldElement):
    """Text field widget

    Args:
    
        name (string): input's name.
        required (bool, optional): set required attribute. Defaults to False.
        disabled (bool, optional): set disabled attribute. Defaults to False.
        readonly (bool, optional): set readonly attribute. Defaults to False.
        placeholder (string, optional): set placeholder. Defaults to None.
        input_type (str, optional): input's type "text", "password",...etc. Defaults to 'text'.
        validators (list[Validator], optional): add validators (auto add RequiredValidator if required). Defaults to None.
        
    """
    input_type = ValidProp(str)
    
    def __init__(self, name, required=False, disabled=False, readonly=False, placeholder=None, input_type='text', validators=None):
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required, validators=validators)
        self.input_type = input_type
        self.attrs.update({'type': input_type})
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        self.input = Element('input', **self.attrs)
        
        # validate on submit
        self.validate()
        
        # ui
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.message:
            wrapper.append(Element('div', self.error.message, _class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
        
    @property
    def data(self):
        return self.form_data
        
    @data.setter
    def data(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError(f'{self.name} must be a string!')
        self.attrs.update({'value': value})
        self.input.attrs.update({'value': value})
        self._data = value
        
class TextAreaField(FieldElement):
    rows = ValidProp(int)
    
    def __init__(self, name, rows=None, required=False, disabled=False, readonly=False, placeholder=None):
        """Textarea field widget
        
        Args:
        
            name (string): textarea's name.
            rows (int, optional): textarea's rows. Defaults to None.
            required (bool, optional): set required attribute. Defaults to False.
            disabled (bool, optional): set disabled attribute. Defaults to False.
            readonly (bool, optional): set readonly attribute. Defaults to False.
            placeholder (string, optional): set placeholder. Defaults to None.
        """
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required)
        self.rows = rows
        if self.rows:
            self.attrs.update({'rows': self.rows})
        
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        self.input = Element('textarea', **self.attrs)
        # validate
        self.validate()
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.status:
            wrapper.append(Element('div', self.error.message, _class='ui basic red pointing prompt label transition visible'))
        self.append(wrapper)
        
    @property
    def data(self):
        return self.form_data
        
    @data.setter
    def data(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError(f'{self.name} must be a string!')
        self.input.inner_text = value
        self._data = value
        
class TextAreaSummernoteField(FieldElement, ReqInjectScriptMixin):
    rows = ValidProp(int)
    
    def __init__(self, name, rows=None, required=False, disabled=False, readonly=False, placeholder=None):
        """Textarea summernote field (rich text editor)

        Args:
        
            name (string): textarea's name.
            rows (int, optional): textarea's rows. Defaults to None.
            required (bool, optional): set required attribute. Defaults to False.
            disabled (bool, optional): set disabled attribute. Defaults to False.
            readonly (bool, optional): set readonly attribute. Defaults to False.
            placeholder (string, optional): set placeholder. Defaults to None.
        """
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required)
        self.rows = rows
        if self.rows:
            self.attrs.update({'rows': self.rows})
        
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        self.input = Element('textarea', **self.attrs, hide_id=False)
        # validate
        self.validate()
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.status:
            wrapper.append(Element('div', _class='ui basic red pointing prompt label transition visible', inner_text=self.error.message))
        self.append(wrapper)
        self.inject_script = f'load_summernote_editor("{self.input.id}", "{self.placeholder}");'
        
    @property
    def data(self):
        return self.form_data
        
    @data.setter
    def data(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError(f'{self.name} must be a string!')
        self.input.inner_text = value
        self._data = value
        
class UploadField(FieldElement):
    def __init__(self, name, required=False, disabled=False, readonly=False, placeholder=None, validators=None):
        """Upload field widget

        Args:
            name (string): input's name
            required (bool, optional): set required attribute. Defaults to False.
            disabled (bool, optional): set disabled attribute. Defaults to False.
            readonly (bool, optional): set readonly attribute. Defaults to False.
            placeholder (string, optional): set placeholder. Defaults to None.
            validators (list[Validator], optional): add validators (auto add RequiredValidator if required). Defaults to None.
        """
        super().__init__('', name=name, placeholder=placeholder, disabled=disabled, readonly=readonly, required=required, validators=validators)
        self.attrs.update({'type': 'file'})
        label = Element('label', inner_text=self.name.title(), _for=self.name)
        self.input = Element('input', **self.attrs)
        
        # validate on submit
        self.validators.append(UploadValidator())
        self.validate()
        
        # ui
        wrapper = Field(label, self.input, required=self.required, disabled=self.disabled, error=self.error.status)
        if self.error.message:
            wrapper.append(Element('div', _class='ui basic red pointing prompt label transition visible', inner_text=self.error.message))
        self.append(wrapper)
    
    @property
    def form_data(self):
        fs = request.files[self.name]
        return fs if fs.filename != '' else None
    
    @property
    def data(self):
        return self.form_data
    
    @property
    def filename(self):
        if self.data:
            return self.data.filename
        
    @property
    def file_ext(self):
        if self.data:
            file_ext = os.path.splitext(secure_filename(self.data.filename))[1]
            return file_ext
        
    @property
    def content_type(self):
        if self.data:
            return self.data.content_type
    
    def save_file(self, folder_name, filename):
        filename = filename if filename else self.data.filename
        self.data.save(
            os.path.join(
                current_app.root_path, 
                'static', 
                current_app.config['FLASK_UIO_UPLOAD_PATH'], 
                folder_name,
                secure_filename(filename)
            )
        )