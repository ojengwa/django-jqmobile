from django import template
from django.contrib.admin.templatetags.admin_modify import prepopulated_fields_js as pfj

register = template.Library()

prepopulated_fields_js = register.inclusion_tag('jqmobile/prepopulated_fields_js.html', takes_context=True)(pfj)
