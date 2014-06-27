from django.db import models
from django.core.exceptions import ValidationError
import simplejson
from django.conf import settings

class MenuItemEncoder(object):
    def __init__(self, menu_items):
        self._fields = {'caption': (True, basestring), 'url': (True, basestring), 'children': (False, None),}
        self.menu_items = menu_items
        self.root = None        
    
    def encode_single_object(self, obj):
        # First check that we don't have a circular dependency.
        obj.clean()
        
        if obj in self.encoded:
            raise ValidationError("MenuItem's cannot have circular dependencies.")
        self.encoded.add(obj)
        
        data = {}
        for field_name, field_info in self._fields.iteritems():
            field_required, field_class = field_info
            
            if hasattr(obj, field_name):
                field = getattr(obj, field_name)
                if field_class is None:
                    if isinstance(field, list):                        
                        field = [self.encode_single_object(x) for x in field]
                    elif field is not field_class:
                        raise ValidationError('MenuItem {0} should be a list of MenuItems instead got {1}'.format(field_name, type(field)))
                elif not isinstance(field, field_class):
                    raise ValidationError('MenuItem incorrect type {0}. {1} expected type {2}'.format(type(field), field_name, field_class))
                data[field_name] = field
            elif field_required:
                raise ValidationError('MenuItem missing required field. {0}'.format(field_name))
        return data
    
    def encode(self):
        self.encoded = set()
        self.root = [self.encode_single_object(i) for i in self.menu_items]
        return simplejson.dumps(self.root)

class MenuItemDecoder(object):
    def __init__(self, json):
        self._json = json
        self.root = []
        self.item_keys = ['caption', 'url']
        
    def decode_single_object(self, item):
        menu_item = MenuItem(**dict((k, item[k]) for k in self.item_keys))
        
        if "children" in item:
            item_children = item['children']
            if item_children:
                children = [self.decode_single_object(x) for x in item_children]
                menu_item.add_children(children)
            elif item_children is not None:
                if not isinstance(item_children, list):
                    raise AttributeError('MenuItem children must be a list of MenuItem instances. Got type.')
        return menu_item
    
    def decode(self):
        self._json_root = simplejson.loads(self._json)
        self.root = [self.decode_single_object(x) for x in self._json_root]
        for x in self.root:
            x.set_depth(0, True)
        return self.root

def flatten_items(items):
    for item in items:
        yield item.flatten()
        if item.children:
            for x in flatten_items(item.children):
                yield x

class MenuItem(object):
    def __init__(self, caption, url):
        self.caption = caption
        self.url = url
        self.children = None
        self.depth = 0
    
    def set_depth(self, d, deep=False):
        self.depth = d
        if deep and self.children:
            for child in self.children:
                child.set_depth(self.depth + 1, deep)
    
    def clean(self):
        level = self.depth + 1
        if not self.caption:
            if self.url:
                raise ValidationError('Menu Item ({0}) at level {1}: caption is required.'.format(self.url, level))
            else:
                raise ValidationError('Menu Item at level {0}: both caption and url are required.'.format(level))
            
        if not self.url:
            raise ValidationError('Menu Item {0} at level {1}: url is required.'.format(self.caption, level))
    
    def flatten(self):
        data = {
            'caption': self.caption,
            'url': self.url,
            'depth': self.depth,
        }
        return data
        
    def add_child(self, child):
        if not isinstance(child, MenuItem):
            raise AttributeError('MenuItem children must be a list of MenuItem instances.')
        if not self.children:
            self.children = []
        self.children.append(child)
        child.set_depth(self.depth + 1)
    
    def add_children(self, children):
        if not isinstance(children, list):
            raise AttributeError('MenuItem children must be a list of MenuItem instances.')
            for child in self.children:
                child.set_depth(self.depth + 1)
            if not isinstance(child, MenuItem):
                raise AttributeError('MenuItem children must be a list of MenuItem instances.')
        
        self.children = children
        
        
    '''

    <menu-items> := {
                "caption": RegexValidator,
                "location": (URLValidator, ),
                "children": [
                    <menu-items>
                ]
            }
        }

    '''
    def toJSON(self):
        s = Serializer(self, {'caption': (True, basestring), 'url': (True, basestring), 'children': (False, None),})
        return s

# TODO: Add is_dirty flag to prevent having to serialize after every insert.
class Menu(models.Model):
    title = models.CharField(max_length=50)
    schema = models.TextField(blank=True, default='')
    
    def get_items(self):
        if hasattr(self, '_items'):
            return getattr(self, '_items')
        
        _items = []
        
        if self.schema:
            decoder = MenuItemDecoder(self.schema)
            _items = decoder.decode()        
        setattr(self, '_items', _items)
        return _items
    
    items = property(get_items)
    
    def add_item(self, item, parent_item=None):
        items = self.items
        if parent_item:
            parent_item.add_child(item)
        else:
            items.append(item)
        self.clean_menu_items()
    
    def get_max_depth(self):
        SIMPLE_MENUS_CONFIG = getattr(settings, 'SIMPLE_MENUS_CONFIG', None)
        MAX_DEPTH = None
        
        if SIMPLE_MENUS_CONFIG:
            MAX_DEPTH = SIMPLE_MENUS_CONFIG.get('MAX_DEPTH')
        
        if MAX_DEPTH is None:
            MAX_DEPTH = 2        
        
        return MAX_DEPTH
        
    def __unicode__(self):
        return 'Menu: {0}'.format(self.title)
    
    def load_schema(self, schema):
        self.schema = schema
        return self.items
        
    def get_flattened(self):
        items = self.items
        return [x for x in flatten_items(items)]
    
    def clean(self):
        self.clean_menu_items()
        return super(Menu, self).clean()
    
    def save(self, *args, **kwargs):
        return super(Menu, self).save(*args, **kwargs)
    
    def clean_menu_items(self):
        items = self.items
        encoder = MenuItemEncoder(items)
        self.schema = encoder.encode()
        
    def build_links(self):
        from simple_menus.utils import build_link_select
        return build_link_select()
        