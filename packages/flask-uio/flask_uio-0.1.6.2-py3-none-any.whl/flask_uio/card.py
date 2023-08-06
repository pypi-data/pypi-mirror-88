from flask_uio.func import get_word
from .element import Element
from .prop import IntProp, ValidProp

class Card(Element):
    """Card widget

    Args:
    
        url (string, optional): link url. Defaults to None.
    
    Defaults:

        If url, tag_name='a' or else 'div'
        class='ui card'
    """
    
    url = ValidProp(str)
    
    def __init__(self, *elements, url=None, **attrs):
        super().__init__('div', **attrs)
        self.url = url
        if self.url:
            self.tag_name = 'a'
            self.attrs.update({'href': self.url})
        
        self.css_class = self.attrs.get('_class') or f'ui card'
        self.append(*elements)
        
class CardImage(Element):
    """Card image widget for showing image in card (Card widget's child)

    Args:
    
        src (string): path to image.
        
    Defaults:

        class='image'
    """
    src = ValidProp(str)
    
    def __init__(self, src):
        super().__init__('div')
        self.src = src
        self.css_class = 'image'
        self.append(Element('img', _src=src))
        
class Cards(Element):
    """Cards widget for managing multiple cards

    Args:
    
        nb_card (string, optional): number of cards. Defaults to None.

    Raises:
    
        Exception: If child is not Card object.
    """
    
    nb_card = IntProp()
    
    def __init__(self, *cards, nb_card=None, **attrs):
        
        super().__init__('div', **attrs)
        self.nb_card = nb_card
        opt = ''
        if self.nb_card:
            opt += ' ' + get_word(self.nb_card)
        
        self.css_class = self.attrs.get('_class') or f'ui{opt} cards'
        
        for card in cards:
            if not isinstance(card, Card):
                raise Exception('Invalid Card Object.')
            card.css_class.replace('ui ', '')
            self.append(card)
        
class CardContent(Element):
    """Card content widget used for adding content to card
    
    Defaults:
    
        class='content'
    """
    def __init__(self, *cards, **attrs):
        super().__init__('div', **attrs)
        self.css_class = self.attrs.get('_class') or 'content'
        self.append(*cards)
        
class CardContentHeader(Element):
    """Card content header widget 
    add header to card content

    Args:
        title (string): header's title
        
    Defaults:

        class='header'
    """
    def __init__(self, title, **attrs):
        super().__init__('div', inner_text=title, **attrs)
        self.css_class = self.attrs.get('_class') or 'header'
        
class CardContentMeta(Element):
    """Card content meta widget 
    add meta to card content

    Args:
    
        text (string): meta text
        
    Defaults:

        class='meta'
    """
    def __init__(self, text, **attrs):
        super().__init__('div', text, **attrs)
        self.css_class = 'meta'
        
class CardContentDesc(Element):
    """Card content description widget 
    add description to card content

    Args:
    
        text (string): description
        
    Defaults:

        class='description'
    """
    def __init__(self, text, **attrs):
        super().__init__('div', text, **attrs)
        self.css_class = 'description'
        