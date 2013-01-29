from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackthon.views.home', name='home'),
    # url(r'^hackthon/', include('hackthon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'extra_context': {'section': 'main'}, 'template': 'default.html'}),
    (r'^fluid/$', 'direct_to_template', {'extra_context': {'section': 'main'}, 'template': 'fluid.html'}),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT,'show_indexes': True}),
        url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,'show_indexes': True}),
    )
