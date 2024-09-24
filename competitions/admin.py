from django.contrib import admin

from competitions.models import City, Competition, CompetitionInSeason, CompetitionLevel, Match, Season, Team

admin.site.register(City)
admin.site.register(Competition)
admin.site.register(CompetitionInSeason)
admin.site.register(CompetitionLevel)
admin.site.register(Match)
admin.site.register(Season)
admin.site.register(Team)
