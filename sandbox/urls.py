from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import mobileadmin
mobileadmin.autoregister()

urlpatterns = patterns('',
    (r'^admin/',        include(admin.site.urls)),
    (r'^ma/',           include(mobileadmin.sites.site.urls)),
    (r'^grappelli/',    include('contrib.grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(.*)$' % settings.MEDIA_URL[1:], 
            'django.views.static.serve', {'document_root': 'media'}),
    )
