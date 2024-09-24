from django.contrib import admin
from accounts.models import *


class ProfileRefereeAdmin(admin.ModelAdmin):
    list_display = ['user', 'referee']
    list_display_links = ['user', 'referee']
    ordering = ['user__username']
    search_fields = ['user__username', 'referee__name', 'referee__surname']


class ProfileManagerAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']
    ordering = ['user__username']
    search_fields = ['user__username']


admin.site.register(ProfileReferee, ProfileRefereeAdmin)
admin.site.register(ProfileManager, ProfileManagerAdmin)