from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dumpsteroverflow.do_core.views.home', name='home'),
    url(r'^overflow/(?P<points>\d+)/$', 'dumpsteroverflow.do_core.views.overflow', name='overflow'),
    url(r'^admin/', include(admin.site.urls)),
)
