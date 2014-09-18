# -*- coding: utf-8 -*-
#
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from models import UserProfile, UserProject, SponsorProfile, UserProject


class UserProfileAdmin(admin.ModelAdmin):
    #fields = ('user','username', 'user_skills', 'user_role', 'has_idea', 'text_idea')
    list_display = ('user',  'username', 'user_skills', 'user_role', 'has_idea', 'text_idea', 'confirmed')


class UserAdminCustom(UserAdmin):
    list_display = ('email', 'get_role', 'get_name', 'get_skills', 'in_team', 'is_staff', 'is_active', 'date_joined')
    ordering = ['-date_joined']

    def get_name(self, obj):
        return obj.profile.username
    get_name.admin_order_field  = 'profile'  #Allows column order sorting
    get_name.short_description = u'Имя'  #Renames column head

    def get_role(self, obj):
        return obj.profile.user_role
    get_role.admin_order_field  = 'profile__user_role'  #Allows column order sorting
    get_role.short_description = u'Роль в команде'  #Renames column head

    def get_skills(self, obj):
        return obj.profile.user_skills
    get_skills.admin_order_field  = 'profile__user_skills'  #Allows column order sorting
    get_skills.short_description = u'Навыки'  #Renames column head

    def in_team(self, obj):
        if obj.profile.in_team:
            return '<img src="/static/admin/img/icon-yes.gif" alt="True">'
        else:
            return '<img src="/static/admin/img/icon-no.gif" alt="False">'
    in_team.short_description = u'В комаде?'  #Renames column head
    in_team.allow_tags = True


class SponsorProfileAdmin(admin.ModelAdmin):
    #fields = ('user','username', 'user_skills', 'user_role', 'has_idea', 'text_idea')
    list_display = ('sponsor_email',)


class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'text_idea')


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProject, UserProjectAdmin)
admin.site.register(SponsorProfile, SponsorProfileAdmin)
