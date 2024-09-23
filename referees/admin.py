from django.contrib import admin
from accounts.models import *
from referees.models import *


class RefereeLicenceAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'level']
    search_fields = ['name', 'level__name']
    list_per_page = 20


class RefereeAdmin(admin.ModelAdmin):
    ordering = ['surname', 'name']
    list_display = ['id', 'name', 'surname', 'city', 'licence', 'rating']
    list_display_links = ['id', 'name','surname']
    list_filter = ['city', 'licence']
    search_fields = ['name', 'surname']
    list_per_page = 20


class UnavailabilityAdmin(admin.ModelAdmin):
    ordering = ['date_from', 'date_to']
    list_display = ['id', 'referee', 'date_from', 'date_to']
    list_display_links = ['id', 'referee']
    list_filter = ['referee']
    search_fields = ['referee__name', 'referee__surname']
    list_per_page = 20


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


admin.site.register(Referee, RefereeAdmin)
admin.site.register(Unavailability, UnavailabilityAdmin)
admin.site.register(RefereeLicence, RefereeLicenceAdmin)
admin.site.register(ProfileReferee, ProfileRefereeAdmin)
admin.site.register(ProfileManager, ProfileManagerAdmin)