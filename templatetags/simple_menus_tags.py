from django import template
from django.template import Node, Library, loader, Context
from django.core.cache import cache
from simple_menus.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context, menu_title, template_name='simple_menus/menu.html', cache_time=None, cache_key=None):
    res = None
    if cache_time is not None:        
        cache_time = int(cache_time)
        if cache_key is None:
            cache_key = 'sm:'+menu_title
        menu = cache.get(cache_key, None)
        if menu is None:
            menu = Menu.objects.get(title=menu_title)
            cache.set(cache_key, menu, cache_time)
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
    t = loader.get_template(template_name)
    
    res = t.render(context)    
    
    return res

@register.simple_tag(takes_context=True)
def show_menuitem(context, item, template_name='simple_menus/menuitem.html'):
    context['menu'] = item
    
    t = loader.get_template(template_name)
    return t.render(context)

@register.tag
def get_menu(parser, token):
    # Usage: {% get_menu 'Menu Name' as 'VariableName' %}
    
    tokens = token.split_contents()
    
    if len(tokens) != 4:
        raise template.TemplateSyntaxError, "%r tag should have 3 arguments" % (tokens[0],)
    
    lookup, skip, var_name = tokens[1:]
        
    if skip != 'as':
        raise template.TemplateSyntaxError, "%r tag's second argument should be as without quotes."
            
    if (not is_quoted(lookup)) or (not is_quoted(var_name)):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tokens[0]
    
    lookup = lookup[1:-1]
        
    return GetMenu(lookup, var_name[1:-1])

class GetMenu(template.Node):
    def __init__(self, lookup, option, var_name):
        self.lookup = lookup
        self.var_name = var_name
    
    def render(self, context):
        try:
            x = Menu.objects.get(title=self.lookup)
        except:
            x = None
        context[self.var_name] = x            
        return ''