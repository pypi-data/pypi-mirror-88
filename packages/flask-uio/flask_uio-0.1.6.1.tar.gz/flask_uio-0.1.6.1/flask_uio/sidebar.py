from .element import Element
from .mixin import ReqInjectScriptMixin
from .menu import Menu, MenuItem
from .icon import Icon

class SideBar(Element, ReqInjectScriptMixin):
    """Sidebar widget (sidebar_menu, nav_menu, content)
    
    Example: append sidebar_menu::
    
        sidebar = uio.SideBar()
        sidebar.sidebar_menu.append(
            uio.Image(url_for('static', filename='vlogo.png'), _class='ui small centered image'),
            uio.MenuHeaderItem('Brand Name'),
            uio.MenuItem('Admin', url='admin'),
            uio.MenuItem('CRM', url='crm'),
            uio.MenuItem('CUS', url='cus'),
        )
    
    Example: append nav_menu::
    
        sidebar.nav_menu.append(
            uio.MenuHeaderItem('Example'),
            uio.MenuItem('System'),
            uio.MenuItem('Resource'),
            uio.RightMenu(
                uio.MenuItem('User Name', 'account', uio.Icon('user icon')),
                uio.MenuItem('Logout', 'logout', uio.Icon('sign out alternate icon'))    
            ),
        )
        
        
    """
    def __init__(self):
        super().__init__('')
        self.sidebar_menu = Menu(_class='ui sidebar inverted vertical menu', hide_id=False)
        self.content = Element('div', _class='pusher')
        self.nav_menu = Menu(_class='ui primary inverted large stackable menu custom')
        self.toggle = MenuItem('', '', icon=Icon('bars icon'), hide_id=False)
        self.nav_menu.append(self.toggle)
        # combined
        self.content.append(self.nav_menu)
        self.append(self.sidebar_menu, self.content)
        self.inject_script = f'$("#{self.toggle.id}").click(function () {{$("#{self.sidebar_menu.id}").sidebar("toggle");}})'