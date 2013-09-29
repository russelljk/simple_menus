from django import template

from django.template.defaulttags import url, URLNode
from django.template import Node

from simple_menus.models import Menu, MenuItem

register = template.Library()

def show_menu(context, menu_title):
    menu = Menu.objects.get(title=menu_title)
    context['menu'] = menu
    return context

register.inclusion_tag('simple_menus/menu.html', takes_context=True)(show_menu)

def show_menuitem(context, item):
    context['menu'] = item
    return context

register.inclusion_tag('simple_menus/menuitem.html', takes_context=True)(show_menuitem)
