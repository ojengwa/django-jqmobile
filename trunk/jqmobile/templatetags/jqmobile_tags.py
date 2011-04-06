# -*- coding: utf-8 -*-

import re, os
from django import template
from django.conf import settings
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _
#from django.core.urlresolvers import reverse

register = template.Library()

def form_flipswitch(field):
    if field.field.value() == True:
        checked = ' selected="selected"'
        unchecked = ''
    else:
        checked = ''
        unchecked = ' selected="selected"'
    # Warning: the value of the "off" option is left intentionnaly
    # blank because Django seems to assume that any data (including "off") == True.
    return u"""<label for="%(id)s" class="ui-input-slider">%(label)s</label>\
<select name="%(name)s" id="%(id)s" data-role="slider">\
    <option value=""%(unchecked)s>%(off)s</option>\
    <option value="on"%(checked)s>%(on)s</option>\
</select>""" % {
        'id': field.field.auto_id, 
        'label': field.field.label, 
        'name': field.field.html_name,
        'on': _('On'),
        'off': _('Off'),
        'unchecked':  unchecked,
        'checked': checked
        }


def form_datetime(field):
    datetime=field.field
    #on place le titre
    out=u'<label for="%s"><h1>%s</h1></label>' % (datetime.auto_id,datetime.label)
    out+='<table>'
    html=datetime.as_widget()
    
    #on recherche les sous titres
    exp=re.compile('([A-Z][a-z]*.:)')
    res_title=exp.findall(html)
    
    #on recherche les dates et heures corespondantes aux sous titres
    exp=re.compile('([0-9][0-9][:|/][0-9][0-9][:|/][0-9]*[0-9])')
    res_date_hour=exp.findall(html)

    #on met tout on place (sous titre + text )
    i=0
    for title in res_title:
        out+='<tr><td> <label for="%(id)s_%(i)d">%(label)s </label></td><td> <input type="text" value="'% {'label':title,'id':datetime.auto_id,'i':i }
        if i < len(res_date_hour):
            out+='%(value)s"' % {'value':res_date_hour[i]}
        else:
            out+='00/00/00"'
        out+='class="vDateField" id="%(id)s_%(i)d" name="%(name)s_%(i)d"/> </td></tr>' % {'id':datetime.auto_id,'i':i, 'name': field.field.html_name }
        i+=1														

    out+='</table>'
    return out


@register.simple_tag
def render_mobile_field(field):
    html = field.field.as_widget()
    #print dir(field)
    if field.is_checkbox:
        out = form_flipswitch(field)
       #print "-------------------------------------------------------"
       #out = '%s <label for="%s" class="vCheckboxLabel" onclick="javascript:;">%s</label>' % (field.field, field.field.auto_id, field.field.label)
       #print "-------------------------------------------------------"
    elif '<p class="datetime">' in html:
        out = form_datetime(field)
    else:
        out = u'<label for="%s">%s</label> %s%s' % (field.field.auto_id, field.field.label, field.field,str(field.field.errors)[22:-5].replace('<li>', '<div class="errormsg">').replace('</li>', '</div>'))
			
    return out


@register.simple_tag
def get_breadcrumb(field):
	path=field

	exp=re.compile('([A-Z a-z 0-9]+/)')
	sub_path=exp.findall(path)
	out=u'<ul>'
	
	i=1;
	path="/"
	#on parcour l'arborecence
	for page in sub_path:
	
		path+=page #on reconstruit l'arborecence à chaque boucle
		out+='<li><a href="%(path)s"' % {'path':path} #on forme la liste des boutons
		
		if i == len(sub_path):
			out+=' class="ui-btn-active"' #on active le dernier lien
		
		out+='>%(page)s</a></li>' % {'page':page} # on fini la liste
		i+=1	
			
	out+='</ul>'
	return out

