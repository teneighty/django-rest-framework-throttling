from django.conf.urls import include, patterns, url
from django.contrib import admin

import views as v

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^numbers/?$', v.GetNumbers.as_view(), name='numbers'),
    url(r'^chars/?$', v.GetChars.as_view(), name='chars'),
    url(r'^admin/', include(admin.site.urls)),
)

