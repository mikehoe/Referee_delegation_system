from django.contrib import admin
from delegations.models import Delegation


class DelegationAdmin(admin.ModelAdmin):
    list_display = ['match', 'referee', 'referee_role']
    list_display_links = ['match', 'referee']
    ordering = ['match__date_time']
    search_fields = ['referee__name', 'referee__surname', 'match__code']

admin.site.register(Delegation, DelegationAdmin)