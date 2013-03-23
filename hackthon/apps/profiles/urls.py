#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profiles import views


urlpatterns = patterns('',
    #url(r'^edit/$', views.edit_profile,
    #                    name='edit_profile'),
    #url(r'^list/$', views.profile_list,
    #                    name='profile_list'),
    url(r'^register/$', views.register,
                        name='profiles_register'),
    url(r'^register/sponsorship/$', views.sponsorship_register,
                        name='sponsorship_register'),
    #url(r'^(?P<username>\w+)/$', views.profile_detail,
    #                    name='profile_detail'),
    )
