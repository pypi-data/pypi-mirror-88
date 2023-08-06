from flask import url_for, current_app
from .prop import ValidProp
from .element import Body, Head, Html
class FomanticHead(Head):
    """Head widget with Fomantic UI

    Args:
    
        title (string): Page's title.
        elements (list[Element], optional): list of element. Defaults to None.
        links (list[Link], optional): list of link. Defaults to None.
        scripts (list[Script], optional): list of script. Defaults to None.
        summernote (bool, optional): enable summernote. Defaults to False.
            
    """
    summernote = ValidProp(bool)
    
    def __init__(self, title, elements=None, links=None, scripts=None, summernote=False, **attrs):
        super().__init__(title, elements, links, scripts, **attrs)
        
        # get fomantic static folder
        static_folder = current_app.config.get('FLASK_UIO_FOMANTIC_STATIC_FOLDER')
        if static_folder is None:
            static_folder = 'flaskuio.static'
        
        # get & add fomantic css filename
        filename = current_app.config.get('FLASK_UIO_FOMANTIC_CSS_FILENAME')
        if filename is None:
            filename = 'style/semantic.min.css'
        self.append_link(url_for(static_folder, filename=filename))
        
        # add support css for summernote (rich text editor)
        self.summernote = summernote
        if self.summernote:
            self.append_link(url_for('flaskuio.static', filename='vendor/summernote-0.8.18-dist/summernote-lite.min.css'))
        self.append_link(url_for('flaskuio.static', filename='style/main.css'))

class FomanticBody(Body):
    """Body widget with Fomantic UI

    Args:
    
        elements (list[Element], optional): list of element. Defaults to None.
        scripts (list[Script], optional): list of script. Defaults to None.
        summernote (bool, optional): enable summernote. Defaults to False.
        
    """
    
    summernote = ValidProp(bool)
    
    def __init__(self, elements=None, scripts=None, summernote=False, **attrs):
        super().__init__(elements, scripts, **attrs)
        
        # get fomantic static folder
        static_folder = current_app.config.get('FLASK_UIO_FOMANTIC_STATIC_FOLDER')
        if static_folder is None:
            static_folder = 'flaskuio.static'
        
        # get fomantic js filename
        filename = current_app.config.get('FLASK_UIO_FOMANTIC_JS_FILENAME')
        if filename is None:
            filename = 'script/semantic.min.js'
        
        # add script required for fomantic ui
        self.append_script(url_for('flaskuio.static', filename='script/jquery-3.5.1.min.js'))
        self.append_script(url_for('flaskuio.static', filename='script/jquery-dateformat.js'))
        self.append_script(url_for(static_folder, filename=filename))
        self.append_script(url_for('flaskuio.static', filename='script/custom-semantic.js'))
        
        # add support script for summernote (rich text editor)
        self.summernote = summernote
        if self.summernote:
            self.append_script(url_for('flaskuio.static', filename='vendor/summernote-0.8.18-dist/summernote-lite.min.js'))
            self.append_script(url_for('flaskuio.static', filename='script/summernote.js'))
        
class Document(Html):
    """Document widget (HTML)

    Args:
    
        title (string): Page's title.
        summernote (bool, optional): enable summernote. Defaults to False.
        
    More Info:
    
        - See https://fomantic-ui.com/
        - See https://summernote.org/
            
    """
    
    summernote = ValidProp(bool)
    
    def __init__(self, title, summernote=False):
        css_framework = current_app.config.get('FLASK_UIO_CSS_FRAMEWORK') or 'fomanticui'
        if css_framework == 'fomanticui':
            self.head = FomanticHead(title, summernote=summernote)
            self.body = FomanticBody(summernote=summernote)
        