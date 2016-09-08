from django.contrib import admin
from django.conf import settings
from django.templatetags.static import static
from simple_menus.models import Menu
from simple_menus.forms import MenuForm


class MenuAdmin(admin.ModelAdmin):
    list_display = ['title',]
    form = MenuForm

    class Media:
        js = (
            # 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            # 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',
            static('admin/simple_menus/mustache.js'),
            static('admin/simple_menus/admin-jquery-ui-stub.js'),
            static('admin/simple_menus/jquery-ui.min.js'),
            static('admin/simple_menus/simple_menus.js'),
        )
        css = {
            'all': (static('admin/simple_menus/simple_menus.css'),),
        }

admin.site.register(Menu, MenuAdmin)
