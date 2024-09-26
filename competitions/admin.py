from django.contrib import admin
from competitions.models import City, Season, CompetitionLevel, Competition, CompetitionInSeason, Team, Match


class CityAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_per_page = 20


class SeasonAdmin(admin.ModelAdmin):
    ordering = ['-name']
    list_display = ['id', 'name', 'date_of_start', 'date_of_end']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_per_page = 20


class CompetitionLevelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_per_page = 20


class CompetitionAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'level', 'category']
    list_display_links = ['id', 'name', 'level', 'category']
    list_filter = ['level', 'category']
    search_fields = ['name', 'level__name', 'category']
    list_per_page = 20


class CompetitionInSeasonAdmin(admin.ModelAdmin):
    ordering = ['-season__name', 'competition__id']
    list_display = ['id', 'competition', 'season']
    list_display_links = ['id', 'competition', 'season']
    list_filter = ['season', 'competition__level']
    search_fields = ['competition__name', 'season__name']
    list_per_page = 20


class TeamAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id', 'name', 'city', 'contact_person', 'phone', 'email', 'competition_in_season']
    list_display_links = ['id', 'name']
    list_filter = ['competition_in_season', 'city']
    search_fields = ['name', 'city__name', 'competition_in_season__competition__name']
    list_per_page = 20


class MatchAdmin(admin.ModelAdmin):
    ordering = ['date_time']
    list_display = ['id', 'code', 'competition_in_season', 'home_team', 'away_team', 'date_time', 'city']
    list_display_links = ['id', 'home_team', 'away_team']
    list_filter = ['competition_in_season', 'date_time', 'city', 'home_team', 'away_team']
    search_fields = ['code', 'home_team__name', 'away_team__name', 'city__name']
    list_per_page = 20


admin.site.register(City, CityAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(CompetitionLevel, CompetitionLevelAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionInSeason, CompetitionInSeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
