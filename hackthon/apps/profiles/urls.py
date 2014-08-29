#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profiles import views


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/edit/$', views.ProfileEditView.as_view(),
                        name='profile_edit'),
    url(r'^list/$', views.ProifileList.as_view(),
                        name='profile_list'),
    url(r'^register/$', views.register,
                        name='profiles_register'),
    url(r'^register/sponsorship/$', views.sponsorship_register,
                        name='sponsorship_register'),
    url(r'^(?P<pk>\d+)/$', views.ProifileDetail.as_view(),
                        name='profile_detail'),

    url(r'^projects/list/$', views.ProjectList.as_view(),
                        name='project_list'),
    url(r'^projects/create/$', views.ProjectCreateView.as_view(),
                        name='project_create'),
    url(r'^projects/join/$', views.JoinProjectView.as_view(),
                        name='project_left'),
    url(r'^projects/left/$', views.LeftProjectView.as_view(),
                        name='project_join'),
    url(r'^projects/confirm/$', views.ConfirmRegisterView.as_view(),
                        name='project_confirm'),
    url(r'^projects/(?P<pk>\d+)/edit/$', views.ProjectEditView.as_view(),
                        name='project_edit'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetail.as_view(),
                        name='project_detail'),
    url(r'^messages/$', views.messages,
                        name='messages'),
    )
