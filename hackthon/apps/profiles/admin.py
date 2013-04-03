from django.contrib import admin
from models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    #fields = ('user','username', 'user_skills', 'user_role', 'has_idea', 'text_idea')
    list_display = ('user',  'username', 'user_skills', 'user_role', 'has_idea', 'text_idea')



admin.site.register(UserProfile, UserProfileAdmin)
