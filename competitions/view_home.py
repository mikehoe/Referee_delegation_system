from datetime import datetime
from django.shortcuts import render
from .models import CompetitionInSeason, Season


def get_current_season(season_id=None):
    today = datetime.now().date()
    seasons = Season.objects.all()

    if season_id:
        return Season.objects.filter(id=season_id).first()

    current_season = None
    for season in seasons:
        if season.date_of_start <= today <= season.date_of_end:
            current_season = season
            break

    if current_season is None:
        current_season = seasons.order_by('date_of_start').last()

    return current_season

def competitions_in_season(request):
    seasons = Season.objects.all()

    selected_season_id = request.GET.get('season')
    current_season = get_current_season(selected_season_id)

    competitions = []
    if current_season is not None:
        competitions = CompetitionInSeason.objects.filter(season=current_season)

    context = {
        'seasons': seasons,
        'competitions': competitions,
        'current_season': current_season,
    }

    return render(request, 'competitions_in_season.html', context)