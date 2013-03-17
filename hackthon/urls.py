from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackthon.views.home', name='home'),
    # url(r'^hackthon/', include('hackthon.foo.urls')),
)

urlpatterns += patterns('',
    (r'^$', TemplateView.as_view(template_name="default.html")),
    (r'^accounts/', include('profiles.urls')),
    (r'^validate/', include('ajax_validation.urls')),
)

urlpatterns += (
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT,'show_indexes': True}),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT,'show_indexes': True}),
        url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,'show_indexes': True}),
    )
