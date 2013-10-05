from django import template
from django.template import Node, Library, loader, Context

from simple_menus.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context, menu_title, template_name='simple_menus/menu.html'):
    menu = Menu.objects.get(title=menu_title)
    context['menu'] = menu
    
    t = loader.get_template(template_name)
    return t.render(context)

@register.simple_tag(takes_context=True)
def show_menuitem(context, item, template_name='simple_menus/menuitem.html'):
    context['menu'] = item
    
    t = loader.get_template(template_name)
    return t.render(context)


