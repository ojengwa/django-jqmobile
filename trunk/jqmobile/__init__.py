from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import site as main_site
from jqmobile.sites import jqmobile as site


def classlookup(C, name):
    """ 
    From http://www2.lib.uchicago.edu/keith/courses/python/class/5/#attrref 
    """
    if C.__dict__.has_key(name):
        return (1, C.__dict__[name])
    else:
        for b in C.__bases__:
		    success, value = classlookup(b, name)
		    if success:
			    return (1, value)
		    else:
			    pass
        else:
		    return (0, None)


def autodiscover():
    """
    Auto-register all ModelAdmin instances of the default AdminSite
    """
    import copy

    for model, modeladmin in main_site._registry.iteritems():
        admin_class = type(modeladmin.__class__.__name__, (modeladmin.__class__,), {
            'change_form_template': 'jqmobile/change_form.html',
            'change_list_template': 'jqmobile/change_list.html',
            'object_history_template': 'jqmobile/object_history.html',
            'delete_confirmation_template': 'jqmobile/delete_confirmation.html',
            'delete_selected_confirmation_template': 'jqmobile/delete_selected_confirmation.html',
        })
                
        if admin_class == UserAdmin:
            setattr(admin_class, 'add_form_template', 'jqmobile/auth/user/add_form.html')
            setattr(admin_class, 'change_user_password_template', 'jqmobile/auth/user/change_password.html')

        site.register(model, admin_class)




