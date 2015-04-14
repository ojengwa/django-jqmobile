## Limitations ##

Some features will be harder to implement than others, some will simply have to be left behind.

### Change list: Date hierarchy & filters ###

Right now date hierarchy, and filters for change list are not implemented because implementing them "the right way" for mobile device isn't trivial. But we are working on it.

### List actions ###

This is a feature we will seek to implement, but right now the right way to do it is not obvious yet. So we are instead focusing on getting all the basic features working well before giving it a try.

### Inlines tabular ###

Tabular inlines in formset will not be supported because jQuery.mobile doesn't provide a simple way to display tabular data, most likely because tabular data doesn't play so well with the screen size of mobile devices.

For this reason, we use stacked inlines to display tabular inlines.

## Releases ##

### v1.0 (First stable release) ###

  * App Index
  * Change list
  * Change list search
  * Change list pagination
  * Change form
  * Change password form
  * Breadcrumb navigation
  * Recent Actions
  * Object history
  * View object on site
  * Logout
  * Options
  * HTML5 field types

### v1.1 ###

  * List Date hierachy
  * List filters

### v1.2 ###

  * List actions ?
  * themes ?