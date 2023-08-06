__version__ = '0.1.6.2'

from .prop import ValidProp, ValidSequenceProp, IntProp
from .mixin import ReqInjectLinkMixin, ReqInjectScriptMixin
from .element import Element, Link, Script, Head, Body, Html
from .base import Document, FomanticBody, FomanticHead
from .core import CoreElement
from .func import number_dict, get_word
from .token import Token
from .button import Button, LinkButton
from .container import Container
from .route import Route
from .validator import Validator, RequiredValidator, RegexValidator, PhoneValidator, EmailValidator, StringValidator, UploadValidator, DateValidator, DateTimeValidator
from .card import Card, CardContent, Cards, CardContentHeader, CardContentMeta, CardContentDesc, CardImage
from .dropdown import Dropdown, DropdownMenu, DropdownMenuItem
from .divider import Divider
from .form import Form
from .icon import Icon, LinkIcon
from .modal import MessageModal, ConfirmModal
from .image import Image, LinkImage
from .text import Text
from .breadcrumb import Breadcrumb, BreadcrumbDividerIcon, BreadcrumbSection
from .message import Message
from .field import Field, UploadField, DropDownField, QueryDropDownField, TextField, TextAreaField, TextAreaSummernoteField, CheckBoxField, DateField, DateTimeField
from .table import Table, TableColItem, TableDateItem, TableDateTimeItem, TableStaticLinkItem
from .segment import Segment, Segments
from .grid import Grid, GridColumn, GridRow
from .menu import Menu, MenuActiveItem, MenuDisableItem, MenuHeaderItem, MenuItem, RightMenu
from .sidebar import SideBar

class FlaskUIO(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def get_engine(self, dbname):
        from flask import current_app
        from sqlalchemy import create_engine
        uris = current_app.config.get('SQLALCHEMY_DATABASE_URI_DICT')
        engine = create_engine(uris.get(dbname))
        return engine
    
    def init_app(self, app):
        from flask import Blueprint, jsonify, current_app
        from sqlalchemy.orm import scoped_session, sessionmaker
        
        app.config.setdefault('FLASK_UIO_CSS_FRAMEWORK', 'fomanticui')
        app.config.setdefault('FLASK_UIO_FOMANTIC_STATIC_FOLDER', None)
        app.config.setdefault('FLASK_UIO_FOMANTIC_CSS_FILENAME', None)
        app.config.setdefault('FLASK_UIO_FOMANTIC_JS_FILENAME', None)
        app.config.setdefault('FLASK_UIO_DATE_FORMAT', '%Y-%m-%d')
        app.config.setdefault('FLASK_UIO_DATETIME_FORMAT', '%Y-%m-%d %H:%M:%S.%f')
        app.config.setdefault('FLASK_UIO_DATE_DISPLAY_FORMAT', '%d-%b-%Y')
        app.config.setdefault('FLASK_UIO_DATETIME_DISPLAY_FORMAT', '%d-%b-%Y, %I:%M %p')
        app.config.setdefault('FLASK_UIO_DATE_JS_FORMAT', 'dd-MMM-yyyy')
        app.config.setdefault('FLASK_UIO_DATETIME_JS_FORMAT', 'dd-MMM-yyyy, hh:mm a')
        app.config.setdefault('FLASK_UIO_MAX_CONTENT_LENGTH', 10 * 1024 * 1024)
        app.config.setdefault('FLASK_UIO_UPLOAD_EXTENSIONS', ['.jpeg', '.jpg', '.png', '.gif', '.pdf', '.xlsx', 'xls', '.csv'])
        app.config.setdefault('FLASK_UIO_UPLOAD_PATH', None)
        app.config.setdefault('FLASK_UIO_API_SERVER', 'http://0.0.0.0:5000')
        app.config.setdefault('FLASK_UIO_FERNET_SECRET_KEY', None)
        app.config.setdefault('SQLALCHEMY_DATABASE_URI_DICT', None)
        
        flaskuio = Blueprint('flaskuio', __name__, static_folder='static', url_prefix='/flaskuio')
        
        @flaskuio.route('/dropdown/<string:e_db>/<string:e_sql>')
        def query_dropdown(e_db, e_sql):
            try:
                secret_key = current_app.config.get('FLASK_UIO_FERNET_SECRET_KEY')
                if secret_key is None:
                    raise Exception('Required Fernet Secret Key.')
                
                token = Token(str(secret_key).encode())
                
                # database 
                dbname = token.decrypt(e_db)
                engine = self.get_engine(dbname)
                db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

                # sql
                sql = token.decrypt(e_sql)
                
                # process data
                options = [{'id': '', 'name': 'Select One'}]
                query = db_session.execute(sql)
                for record in query:
                    options.append({'id': record[0], 'name': record[1]})
                    
                return jsonify(options)
            except Exception as ex:
                return str(ex), 400
            
        @flaskuio.route('/relationship_dropdown/<string:e_db>/<string:e_sql>/<string:value>')
        def query_relationship_dropdown(e_db, e_sql, value):
            try:
                secret_key = current_app.config.get('FLASK_UIO_FERNET_SECRET_KEY')
                if secret_key is None:
                    raise Exception('Required Fernet Secret Key.')
                
                token = Token(str(secret_key).encode())
                
                # database 
                dbname = token.decrypt(e_db)
                engine = self.get_engine(dbname)
                db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
                
                # sql
                sql = token.decrypt(e_sql)
                
                # check values
                api_values = value[:len(value)-2].split('$$')
                for v in api_values:
                    kv = v.split('_')
                    if len(kv) > 0:
                        sql = sql.replace(kv[0], '0' if str(kv[1]).isspace() else kv[1])
                
                # process data
                options = [{'id': '', 'name': 'Select One'}]
                query = db_session.execute(sql)
                for record in query:
                    options.append({'id': str(record[0]), 'name': str(record[1])})
                    
                return jsonify(options)
            except Exception as ex:
                return str(ex), 400
        
        app.register_blueprint(flaskuio)