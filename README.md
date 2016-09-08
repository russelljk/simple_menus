# Simple Menus

A relatively simple to use nested menu's app for Django 1.10

## Installation

Add `simple_menus` to your installed apps.

```python
INSTALLED_APPS = (
	...
	'simple_menus',
	...
)
```

Then run migrations:

	./manage.py migrate

### Configuration

In `project/settings.py` add your configuration:

```python
SIMPLE_MENUS_CONFIG = {
    'MAX_DEPTH': 2,
    'MAX_ITEMS': 30,
    'SITEMAPS_LOCATION': 'project.sitemaps',
    'SITEMAPS_NAME': 'sitemaps',
    'SITEMAPS_EXCLUDE': ['appthree'],
}
```

 * `MAX_DEPTH` - Maximum nesting depth of menu items.
 * `MAX_ITEMS` - Maximum number of items to allow in a menu.

The in `project/sitemaps.py` you have your sitemaps declarations:

```python
sitemaps = {
	'appone': AppOneSitemap,
	'apptwo': AppTwoSitemap,
	'appthree': AppThreeSitemap,
}
```

Optionally Simple Menus can pull links in from your Sitemaps and show them in the admin.

 * `SITEMAPS_LOCATION` - The path to import your sitemaps.
 * `SITEMAPS_NAME` - The name of the dict containing your site maps
 * `SITEMAPS_EXCLUDE` - Sitemaps to exclude, in the above example AppThreeSitemap's links will be excluded.
