from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import jqmobile

admin.autodiscover()
jqmobile.autodiscover()


urlpatterns = patterns('',
    (r'^admin/',        include(admin.site.urls)),
    (r'^ma/',           include(jqmobile.site.urls)),
    (r'^grappelli/',    include('contrib.grappelli.urls')),
    (r'^$',             'django.views.generic.simple.redirect_to', {'url': '/ma/'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(.*)$' % settings.MEDIA_URL[1:], 
            'django.views.static.serve', {'document_root': 'media'}),
    )
