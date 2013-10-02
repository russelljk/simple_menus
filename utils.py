#from django.utils.safestring import mark_safe    

def build_link_select():
    '''
    Build groups of links based on what is in the site's sitemaps.
    
    'Genre': {
        [   ('Item 0', '/path/to/item0'),
            ('Item 1', '/path/to/item1') ]
    }
    '''
    from mylibs.helpers.caching import cache_safe_set, cache_safe_get        
    from django.conf import settings
    import re
    ITEM_TYPE_RE = re.compile(ur'^[a-zA-Z]+\:\s+(.+)$')
    
    SIMPLE_MENUS_CONFIG = getattr(settings,  'SIMPLE_MENUS_CONFIG', None)
    groups = {}
    
    if SIMPLE_MENUS_CONFIG is None:
        return groups
    
    SITEMAPS_LOCATION = SIMPLE_MENUS_CONFIG.get('SITEMAPS_LOCATION', None)
    SITEMAPS_NAME = SIMPLE_MENUS_CONFIG.get('SITEMAPS_NAME', None)
    SITEMAPS_EXCLUDE = SIMPLE_MENUS_CONFIG.get('SITEMAPS_EXCLUDE', set())
    
    if SITEMAPS_LOCATION is None:
        return groups
    
    _module = __import__(SITEMAPS_LOCATION, globals(), locals(), [ SITEMAPS_NAME ], 0)
    _sitemaps = _module.sitemaps
    
    if not isinstance(_sitemaps, dict):
        return groups
    
    cache_groups = cache_safe_get('build_link_select')
    
    if cache_groups is not None:
        return cache_groups
    
    for name in _sitemaps:        
        if name in SITEMAPS_EXCLUDE:
            continue
        try:
            _SitemapClass = _sitemaps[name]
            locations = []
            sitemap = _SitemapClass()
            for item in sitemap.items():
                item_name = unicode(item)
                re_groups = ITEM_TYPE_RE.findall(item_name)
                if re_groups:
                    item_name = re_groups[0]
                loc = (item_name, sitemap.location(item))
                locations.append(loc)
            if locations:
                groups[name.capitalize()] = locations
        except:
            pass
    cache_safe_set('build_link_select', groups, 1800)
    
    return groups