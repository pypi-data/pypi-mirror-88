from flask_uio import Element
import pytest

def test_has_attributes_when_create_an_element():
    div = Element('div')
    assert hasattr(div, 'tag_name')
    assert hasattr(div, 'css_class')
    assert hasattr(div, 'attrs')
    assert hasattr(div, 'inner_text')
    assert hasattr(div, '_inner_elements')
    assert hasattr(div, '_prev_elements')
    assert hasattr(div, '_next_elements')
    assert hasattr(div, 'self_closing_tag')
    assert hasattr(div, 'hide_id')

testcase1 = [
    (
        Element('div'), 
        {
            'tag_name': 'div',
            'hide_id': True,
            'attrs': {},
            'css_class': None,
            'inner_text': None,
            'self_closing_tag': False,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
        }
    ),
    (
        Element('span', 'testing'),
        {
            'tag_name': 'span',
            'hide_id': True,
            'attrs': {},
            'css_class': None,
            'inner_text': 'testing',
            'self_closing_tag': False,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
        }
    ),
    (
        Element('div', 'testing', False),
        {
            'tag_name': 'div',
            'hide_id': False,
            'attrs': {},
            'css_class': None,
            'inner_text': 'testing',
            'self_closing_tag': False,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
        }
    ),
    (
        Element('br', self_closing_tag=True),
        {
            'tag_name': 'br',
            'hide_id': True,
            'attrs': {},
            'css_class': None,
            'inner_text': None,
            'self_closing_tag': True,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
        }
    ),
    (
        Element('form', _class='ui form', _method='POST', _action='index.php'),
        {
            'tag_name': 'form',
            'hide_id': True,
            'attrs': {'_class': 'ui form', '_method': 'POST', '_action':'index.php'},
            'css_class': 'ui form',
            'inner_text': None,
            'self_closing_tag': False,
            '_inner_elements': [],
            '_prev_elements': [],
            '_next_elements': [],
        }
    )
]
@pytest.mark.parametrize('test, expect', testcase1)
def test_element_has_valid_attribute_value(test, expect):
    assert getattr(test, 'tag_name') == expect['tag_name']
    assert getattr(test, 'hide_id') == expect['hide_id']
    assert getattr(test, 'attrs') == expect['attrs']
    assert getattr(test, 'css_class') is expect['css_class']
    assert getattr(test, 'inner_text') is expect['inner_text']
    assert getattr(test, 'self_closing_tag') == expect['self_closing_tag']
    assert getattr(test, '_inner_elements') == expect['_inner_elements']
    assert getattr(test, '_prev_elements') == expect['_prev_elements']
    assert getattr(test, '_next_elements') == expect['_next_elements']

testelement = Element('span', inner_text='Element for testing')

def test_append():
    e = Element('div')
    e.append(testelement)
    assert testelement in e._inner_elements
    
def test_append_prev():
    e = Element('div')
    e.append_prev(testelement)
    assert testelement in e._prev_elements
    
def test_append_next():
    e = Element('div')
    e.append_next(testelement)
    assert testelement in e._next_elements
    
def test_find_element():
    
    class Div(Element):
        def __init__(self):
            super().__init__('div')
    
    class Span(Element):
        def __init__(self):
            super().__init__('span')
            
    e2 = Element('div')
    e2.append(Div())
    e2.append_next(Span())
    
    e1 = Element('div')
    e1.append_prev(e2)
    
    e = Element('div')
    e.append(e1)
    
    result = e.find_element(Div, Span)
    assert len(result) == 2
    
testcase2 = [
    (
        Element('div',
            _class='ui segment',
            inner_text='hello world',
        ),
        '<div class="ui segment">hello world</div>'
    ),
    (
        Element('input',
            _class='ui input',
            _type='email',
            _name='email_address',
            _required=True,
            hide_id=False,
        ),
        '<input id="replaced_id" class="ui input" type="email" name="email_address" required="True"></input>'
    ),
    (
        Element('br', self_closing_tag=True),
        '<br />'
    ),
    (
        Element('input', _type='text', _value='some value', _name='txt1', hide_id=False, self_closing_tag=True),
        '<input id="replaced_id" type="text" value="some value" name="txt1" />'
    )
]
@pytest.mark.parametrize('test, expect', testcase2)
def test_get_html(test, expect):
    assert test.get_html() == expect.replace("replaced_id", test.id)
    
    
    
    
