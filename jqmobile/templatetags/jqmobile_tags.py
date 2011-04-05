# -*- coding: utf-8 -*-

import re, os
from django import template
from django.conf import settings
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _
#from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def render_mobile_field(field):
    html = field.field.as_widget()

    print dir(field.field)
    if field.is_checkbox:
       #out = '%s <label for="%s" class="vCheckboxLabel" onclick="javascript:;">%s</label>' % (field.field, field.field.auto_id, field.field.label)
	    out = u'<label for="%s" class="ui-input-slider">%s</label> <select name="%s" id="%s" data-role="slider"><option value="off">%s</option><option value="on">%s</option></select>' % (field.field.auto_id, field.field.label, field.field.auto_id, field.field.auto_id, _('On'), _('Off'))
    else:
        out = u'<label for="%s">%s</label> %s' % (field.field.auto_id, field.field.label, field.field)

    return out


