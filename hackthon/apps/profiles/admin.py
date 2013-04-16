from django.contrib import admin
from models import UserProfile, UserProject, SponsorProfile, UserProject


class UserProfileAdmin(admin.ModelAdmin):
    #fields = ('user','username', 'user_skills', 'user_role', 'has_idea', 'text_idea')
    list_display = ('user',  'username', 'user_skills', 'user_role', 'has_idea', 'text_idea', 'confirmed')


class SponsorProfileAdmin(admin.ModelAdmin):
    #fields = ('user','username', 'user_skills', 'user_role', 'has_idea', 'text_idea')
    list_display = ('sponsor_email',)


class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'text_idea')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProject, UserProjectAdmin)
admin.site.register(SponsorProfile, SponsorProfileAdmin)
