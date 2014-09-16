from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

#reg urls
urlpatterns += patterns('',
    url(r'^projects/$', RedirectView.as_view(url='/accounts/projects/list/')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
)

urlpatterns += patterns('',
    #(r'^$', TemplateView.as_view(template_name="default.html")),
    (r'^$', TemplateView.as_view(template_name="new.html")),
    (r'^first/$', TemplateView.as_view(template_name="first.html")),
    (r'^second/$', TemplateView.as_view(template_name="second.html")),
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
