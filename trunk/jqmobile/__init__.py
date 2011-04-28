import os.path
import re


VERSION = (1, 0, 0, 'alpha', 0)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    svn_rev = get_svn_revision()
    if svn_rev != u'SVN-unknown':
        version = "%s %s" % (version, svn_rev)
    return version


def get_svn_revision(path=None):
    """
    Returns the SVN revision in the form SVN-XXXX,
    where XXXX is the revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.

    If path is provided, it should be a directory whose SVN info you want to
    inspect. If it's not provided, this will use the root jqmobile/ package
    directory.
    """
    rev = None
    if path is None:
        import jqmobile
        path = jqmobile.__path__[0]
    entries_path = '%s/.svn/entries' % path

    try:
        entries = open(entries_path, 'r').read()
    except IOError:
        pass
    else:
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return u'SVN-%s' % rev
    return u'SVN-unknown'


try:
    # We need to wrap this into a try/except so the setup script
    # can import the above code without Django environment variables

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

        for model, modeladmin in main_site._registry.iteritems():
            admin_class = type(modeladmin.__class__.__name__, (modeladmin.__class__,), {
                'change_form_template': 'jqmobile/change_form.html',
                'change_list_template': 'jqmobile/change_list.html',
                'object_history_template': 'jqmobile/object_history.html',
                'delete_confirmation_template': 'jqmobile/delete_confirmation.html',
                'delete_selected_confirmation_template': 'jqmobile/delete_selected_confirmation.html',
            })
            
            # we have to recreate inlines too..
            inlines = []
            for inline in modeladmin.inlines:
                inlines.append(type(inline.__name__, (inline,), {
                    # mobiles devices and tabular data don't mix well..
                    'template': 'jqmobile/edit_inline/stacked.html',
                }))
            setattr(admin_class, 'inlines', inlines)

            # Exceptions for User model
            if modeladmin.__class__ == UserAdmin:
                setattr(admin_class, 'add_form_template', 'jqmobile/auth/user/add_form.html')
                setattr(admin_class, 'change_user_password_template', 'jqmobile/auth/user/change_password.html')

            site.register(model, admin_class)
except:
    pass
