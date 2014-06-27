from django import template
from django.template import Node, Library, loader, Context
from mylibs.helpers.caching import smart_cache
from simple_menus.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context, menu_title, template_name='simple_menus/menu.html', cache_time=None, cache_key=None):
    res = None
    if cache_time is not None:        
        cache_time = int(cache_time)
        if cache_key is None:
            cache_key = 'sm:'+menu_title
        menu = smart_cache(cache_key, Menu.objects.get(title=menu_title), cache_time)
    else:
        menu = Menu.objects.get(title=menu_title)
    
    context['menu'] = menu
    
    t = loader.get_template(template_name)
    res = t.render(context)    
        
    return res

@register.simple_tag(takes_context=True)
def render_menu(context, menu, template_name='simple_menus/menu.html'):
    res = None
    context['menu'] = menu
    print context
    t = loader.get_template(template_name)
    
    res = t.render(context)    
    
    return res

@register.simple_tag(takes_context=True)
def show_menuitem(context, item, template_name='simple_menus/menuitem.html'):
    context['menu'] = item
    
    t = loader.get_template(template_name)
    return t.render(context)


