from django.contrib import admin
from django.conf import settings
from simple_menus.models import Menu
from simple_menus.forms import MenuForm

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title',]
    form = MenuForm
    
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',
            settings.STATIC_URL + 'admin/simple_menus/simple_menus.js',
            settings.STATIC_URL + 'admin/simple_menus/mustache.js',
        )
        css = {
            'all': (settings.STATIC_URL + 'admin/simple_menus/simple_menus.css',),
        }

admin.site.register(Menu, MenuAdmin)