# -*- coding: utf-8 -*-

import re, os
from django import template
from django.conf import settings
from django.utils.safestring import SafeString
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR, SEARCH_VAR

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
    out+='<table><tr>'
    
    html=datetime.as_widget()
    errors=(unicode(datetime.errors)).replace('<ul class="errorlist">','<span id="date_errors"><ul class="errorlist">').replace('</ul>','</ul></span>')
    
    #on recherche les sous titres
    exp=re.compile('([A-Z][a-z]*.:)')
    res_title=exp.findall(html)
    
    #on recherche les dates et heures corespondantes aux sous titres   
#   exp=re.compile('(value=".{8,10}")')
    exp=re.compile('value="(.*?)"')
    res_date_hour=exp.findall(html)
#   for i in range(0,len(res_date_hour)):
#   	res_date_hour[i]=res_date_hour[i]
    
    #on cherche les classe corespondante au type de input (le premier trouve est faux, car englobant)
    exp=re.compile('(class="[_A-Za-z0-9-]+")')
    _type=(exp.findall(html))
    #on met tout on place (sous titre + text )
    
    i=0
    for title in res_title:
        out+='<td> <label for="%(id)s_%(i)d">%(label)s </label></td><td>' % {'label':title,'id':datetime.auto_id,'i':i}
        # { <input type="text" %(_type)s value=,'_type':_type[i+1] }
        
        if i < len(res_date_hour):
        	if "Time" in _type[i+1]: #time
        		out+= '<input type="time"'
        	else: #date
        		out+='<input type="date"'
        		
        	out+=' value="%(value)s"' % {'value':res_date_hour[i]}
        elif "Time" in _type[i+1]: #time
            out+='<input type="time" value=""'
        else: #date
        	out+='<input type="date" value=""'
        	
        out+=' id="%(id)s_%(i)d" name="%(name)s_%(i)d"/> </td>' % {'id':datetime.auto_id,'i':i, 'name': field.field.html_name }
        i+=1
    out+='</tr></table>'
    out+= errors
    return out


@register.simple_tag
def render_mobile_field(field):
    html = field.field.as_widget()
    #html=html.replace('<a href="','<span id="button"><a href="').replace('</a>','</a></span>')
    #print (html+ '\n')
    
    
    
#   if field.is_checkbox:
#       out = form_flipswitch(field)
#      #print "-------------------------------------------------------"
#      #out = '%s <label for="%s" class="vCheckboxLabel" onclick="javascript:;">%s</label>' % (field.field, field.field.auto_id, field.field.label)1
#      #print "-------------------------------------------------------"
    if '<p class="datetime">' in html:
        out = form_datetime(field)
    #elif '<option value="off">Off</option> <option value="on">On</option>' in html:
    #	print("on off")

    else:
		#on recupere le possible bouton d'ajout
		exp=re.compile('(<a href=".*></a>$)');
		bottom_button=exp.findall(html);
		href='';		
		#print (html+'\n')
		#on regarde si il y a effectivement un bouton d'ajout
		if(len(bottom_button)>0):
			html=html.replace(bottom_button[0],'')
			exp=re.compile('(<a href=".*;">)');
			href=(exp.findall(bottom_button[0]));
			href[0]=href[0].replace('<a','<a data-role="button" data-icon="plus" id="%(id)s_button"' % {'id':field.field.auto_id});

		out = u'<label for="%(id)s">%(label)s</label> %(objet)s' % {'id':field.field.auto_id, 
        'label':field.field.label,
         'objet':html,
         }
         #on ajout le bouton sous le reste
		if (href!=''):
			out+='<span class="form-button">%(ajout)s %(new)s </a></span>' % {'ajout':href[0], 'new':_("New")}
		elif '<input name="password"' in html:
			out+='<span class="form-button"><a data-role="button" data-icon="gear" href="password" id="%(id)s_button">%(label)s</a></span>' % {
                    'id':field.field.auto_id,
                    'label': _('Change Password'),
                    }
        
		out+='<span id="%(id)s_errors" >%(errors)s</span>' % {'id':field.field.auto_id,'errors':unicode(field.field.errors)}
		
		#inclure le fichier livevalidation_standalone.compressed.js pour des verification en temps reel
    	#if 'type="text"' in html:
        #	out+='<script type="text/javascript">'
        #	if "email" in html:
        #		out+='var %(id)s = new LiveValidation("%(id)s", { validMessage: "%(valid)s" ,wait: 500});\n %(id)s.add(Validate.Presence, {failureMessage: "%(fail)s" });\n %(id)s.add(Validate.Format, {pattern: /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i,failureMessage: "%(fail)s" });' % {'id':field.field.auto_id,'valid':"email correct",'fail': "email incorrect"}        		
        #	out+='</script>'
    return out


@register.simple_tag
def get_breadcrumb(field,name=''):
	path = field
	exp = re.compile('([A-Z a-z 0-9]+/)')
	sub_path = exp.findall(path)
	out = u'<div data-role="navbar"><ul class="breadcrumbs">'
	i = 0;
	path = "/"
	last_sub = ''

	#on parcour l'arborecence
	for page in sub_path:
		path +=page #on reconstruit l'arborecence a chaque boucle
		out +='<li><a data-theme="c" href="%(path)s"' % {'path':path} #on forme la liste des boutons
		
		if i == len(sub_path)-1:
            # on active le dernier lien
			out +=' class="ui-btn-active"' 
			
		if i>0 and name != '' and ("user/" in sub_path[i-1] or "group/" in sub_path[i-1]):
			page = unicode(name)
		
		if i ==0:
			out +=' class="ui-btn-home"><span class="hidden">%s</span><span class="home-icon">&nbsp;</span></a></li>' % _('Home')
		else:
			out +='>%(page)s</a></li>' % {'page': page.replace('/', '')} # on fini la liste
		i +=1	
		last_sub =page
	out+='</ul></div>'

	return out
	
@register.simple_tag
def get_back_path(field):
	path=field
	exp=re.compile('([A-Z a-z 0-9]+/)')
	sub_path=exp.findall(path)
	i=1;
	if i < len(sub_path):
		path="/"
		for page in sub_path:
			if i < len(sub_path):
				path+=page
			i+=1
	else:
		path="./"
	#on parcour l'arborecence
	
	return path


# Pagination

def paginator_number(cl, i,):
    theme = ''
    if i == cl.page_num:
        theme = ' data-theme="b"'
    return u'<a href="%s"%s data-role="button">%d</a> ' % (cl.get_query_string({PAGE_VAR: i}), theme, i+1)
paginator_number = register.simple_tag(paginator_number)

def pagination(cl):
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 1

        # If there are 4 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 3:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > ON_EACH_SIDE:
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.extend(range(paginator.num_pages, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    
    #render_to_string(('jqmobile/pagination.html','admin/pagination.html'), {'cl': cl,'pagination_required':pagination_required,'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),'page_range': page_range,'ALL_VAR': ALL_VAR,'1': 1,})
    
    out=render_to_string((
        'jqmobile/pagination.html',
        'admin/pagination.html'
    ), {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    })
    
    return out
register.simple_tag(pagination)
