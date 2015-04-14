# Introduction #

Here you will find the basic configurations required to get you started.

## Installation ##

### Latest official release ###

```
sudo easy_install jqmobile
```

### From source ###

```
svn checkout http://django-jqmobile.googlecode.com/svn/trunk/ django-jqmobile
```

Then make django-jqmobile/jqmobile/ available in your PYTHON path environment variable.

## Configurations ##

### settings.py ###

```

STATICFILES_DIRS = (
    # ...
    '/full/path/to/jqmobile/static/',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'mobileadmin',
)

```

### urls.py ###

```

from django.conf.urls.defaults import *
from django.contrib import admin
import jqmobile

admin.autodiscover()
jqmobile.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^ma/',    include(jqmobile.site.urls)),
)

```