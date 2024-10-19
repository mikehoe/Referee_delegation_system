from django.contrib import admin
from referees.models import *


class RefereeLicenceTypeAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'competition_levels']
    search_fields = ['name', 'competition_levels__name']
    list_per_page = 20


class RefereeAdmin(admin.ModelAdmin):
    ordering = ['licence_type__id', 'profile__user__last_name', 'profile__user__first_name']
    list_display = ['id', 'profile__user__first_name', 'profile__user__last_name', 'city', 'licence_type', 'rating']
    list_display_links = ['id', 'profile__user__first_name', 'profile__user__last_name']
    list_filter = ['licence_type', 'city']
    search_fields = ['profile__user__first_name', 'profile__user__last_name', 'licence_number']
    list_per_page = 20


class UnavailabilityAdmin(admin.ModelAdmin):
    ordering = ['date_from', 'date_to']
    list_display = ['id', 'referee', 'date_from', 'date_to']
    list_display_links = ['id', 'referee']
    list_filter = ['referee']
    search_fields = ['referee__profile__user__last_name', 'referee__profile__user__first_name']
    list_per_page = 20


admin.site.register(Referee, RefereeAdmin)
admin.site.register(Unavailability, UnavailabilityAdmin)
admin.site.register(RefereeLicenceType, RefereeLicenceTypeAdmin)
