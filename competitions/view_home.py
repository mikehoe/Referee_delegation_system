from django.shortcuts import render
from django.utils import timezone
from .models import CompetitionInSeason, Season

def home(request):
    seasons = Season.objects.all()
    competitions = []
    today = timezone.now().date()

    selected_season_id = request.GET.get('season')

    if selected_season_id:
        current_season = Season.objects.filter(id=selected_season_id).first()
    else:
        current_season = None
        for season in seasons:
            if season.date_of_start <= today <= season.date_of_end:
                current_season = season
                break

        if current_season is None:
            current_season = seasons.order_by('date_of_start').last()

    if current_season is not None:
        competitions = CompetitionInSeason.objects.filter(season=current_season)

    context = {
        'seasons': seasons,
        'competitions': competitions,
        'current_season': current_season,
    }

    return render(request, 'home.html', context)