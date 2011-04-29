from django.contrib.admin.sites import AdminSite, site
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import password_change, password_change_done, logout


class MobileAdminSite(AdminSite):
#   login_form = None
    index_template = 'jqmobile/index.html' 
    app_index_template = 'jqmobile/app_index.html'
    login_template = 'jqmobile/login.html'
    logout_template = 'jqmobile/registration/logged_out.html'
    password_change_template = 'jqmobile/registration/password_change_form.html'
    password_change_done_template = 'jqmobile/registration/password_change_done.html'

    

#   def get_urls(self):
#       from django.conf.urls.defaults import patterns, url

#       urls = super(MobileAdminSite, self).get_urls()
#       urls += patterns('',
#           url(r'^my_view/$', self.admin_view(some_view))
#       )
#       return urls
#   def my_view(self, request):
#       # custom view which should return an HttpResponse
#       pass

jqmobile = MobileAdminSite(name='jqmobile')
