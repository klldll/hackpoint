#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profiles import views


urlpatterns = patterns('',
    url(r'^edit/$', views.edit_profile,
                        name='profile_edit'),
    url(r'^list/$', views.ProifileList.as_view(),
                        name='profile_list'),
    url(r'^register/$', views.register,
                        name='profiles_register'),
    url(r'^register/sponsorship/$', views.sponsorship_register,
                        name='sponsorship_register'),
    url(r'^(?P<pk>\d+)/$', views.ProifileDetail.as_view(),
                        name='profile_detail'),
    )
