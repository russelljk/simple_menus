from django.test import TestCase
from simple_menus.models import *
from django.core.exceptions import ValidationError

import os
APP_PATH = os.path.abspath(os.path.dirname(__file__))

class BaseTestCase(TestCase):
    def setUp(self):
        JSON_FILES = {
            'flat_json': 'flat.json',
            'nested_json': 'nested.json',
            'missing_attr_json': 'missing_attr.json',
        }
        
        for name, loc in JSON_FILES.iteritems():
            f = open(APP_PATH + '/testdata/json/' + loc)
            setattr(self, name, f.read())
            f.close()

class DecodeTestCase(BaseTestCase):    
    def test_decode_nested(self):
        decoder = MenuItemDecoder(self.nested_json)
        items = decoder.decode()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsInstance(item, MenuItem)
            self.assertTrue(hasattr(item, 'caption'))
            self.assertTrue(hasattr(item, 'url'))
        item_2 = items[1]
        self.assertEqual(item_2.caption, 'About')
        self.assertTrue(hasattr(item_2, 'children'))
        children = item_2.children
        self.assertEqual(len(children), 2)
        for item in children:
            self.assertIsInstance(item, MenuItem)
            self.assertTrue(hasattr(item, 'caption'))
            self.assertTrue(hasattr(item, 'url'))
    
    def test_decode_encode(self):        
        decoder = MenuItemDecoder(self.flat_json)
        items = decoder.decode()
        
        encoder = MenuItemEncoder(items)
        json = encoder.encode()
        self.assertIsInstance(json, str)
        
    def test_decode_valid(self):        
        decoder = MenuItemDecoder(self.flat_json)
        items = decoder.decode()
        self.assertEqual(len(items), 2)
        for item in items:
            self.assertIsInstance(item, MenuItem)
            self.assertTrue(hasattr(item, 'caption'))
            self.assertTrue(hasattr(item, 'url'))
            
    def test_decode_bad_json(self):
        decoder = MenuItemDecoder(self.missing_attr_json)
        self.assertRaises(KeyError, lambda: decoder.decode())

class MenuTestCase(BaseTestCase):
    
    def load_menu(self, menuname, name):
        menu = Menu()
        menu.title = menuname
        menu.load_schema( name )
        return menu
    
    def test_nested_menu(self):
        menu = self.load_menu( 'MainNested', self.nested_json )
        self.assertTrue(hasattr(menu, '_items'))
        self.assertEqual(len(menu.items), 2)
        
        menu.save()
        
        m = Menu.objects.get(title='MainNested')
        self.assertEqual(m.title, 'MainNested')
        self.assertEqual(len(m.items), 2)
        items = m.items
        item_2 = items[1]
        self.assertEqual(item_2.caption, 'About')
        self.assertTrue(hasattr(item_2, 'children'))
        children = item_2.children
        
        self.assertEqual(len(children), 2)
        
        for item in m.items:
            self.assertIsInstance(item, MenuItem)
    
    def test_add_menuitem(self):
        menu = self.load_menu( 'AddMain', self.flat_json )
        items = menu.items
        
        item = MenuItem('Search', '/search/')        
        menu.add_item(item)
        
        self.assertEqual(len(menu.items), 3)
        
        menu.save()
        
        m = Menu.objects.get(title='AddMain')
        
        self.assertEqual(len(m.items), 3)
        
        for item in m.items:
            self.assertIsInstance(item, MenuItem)
        
        self.assertEqual(m.items[2].caption, item.caption)
        self.assertEqual(m.items[2].url, item.url)
        
    def test_flat_menu(self):
        menu = self.load_menu( 'FlatMain', self.flat_json )
        self.assertTrue(hasattr(menu, '_items'))
        self.assertEqual(len(menu.items), 2)
        
        menu.save()
        
        m = Menu.objects.get(title='FlatMain')
        self.assertEqual(m.title, 'FlatMain')
        self.assertEqual(len(m.items), 2)
        for item in m.items:
            self.assertIsInstance(item, MenuItem)
        
        