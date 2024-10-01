import datetime
from django.core.management.base import BaseCommand
from competitions.models import CompetitionInSeason, Team, Match
from imports.berger_tables import BergerTables


class Command(BaseCommand):
    help = ("It generates volleyball matches for all competitions in given season "
            "according to the system of Berger's tables")

    def add_arguments(self, parser):
        parser.add_argument('season', type=str, help='For example: 2024/2025')

    def handle(self, *args, **kwargs):
        competitions_in_season = CompetitionInSeason.objects.filter(season__name=kwargs['season'])
        berger_tables = BergerTables()
        teams_min = berger_tables.TEAMS_MIN
        teams_max = berger_tables.TEAMS_MAX

        for competition_in_season in competitions_in_season:
            teams = Team.objects.filter(competition_in_season=competition_in_season)
            teams_count = len(teams)

            if teams_count < teams_min or teams_count > teams_max:
                self.stdout.write(
                    f"Skipping {competition_in_season} due to unsupported number of teams "
                    f"(less than {teams_min} or more than {teams_max}): {teams_count}.")
                continue

            # Choose the correct table based on the number of teams.
            proper_berger_table = berger_tables.get_berger_table(teams_count)

            # Creation of matches according to Berger's tables from given start datetime.
            match_number = 1
            match_datetime = Match.get_start_datetime(date_of_start=competition_in_season.season.date_of_start,
                                                        weekday=5, hour=18, minute=0)

            for round_matches in proper_berger_table:

                for home_team_index, away_team_index in round_matches:
                    home_team = teams[home_team_index - 1]
                    away_team = teams[away_team_index - 1]

                    match_code = Match.generate_match_code(competition_in_season, match_number)
                    if  (Match.objects.filter(competition_in_season=competition_in_season)
                            .filter(code=match_code).exists()):
                        self.stdout.write(
                            f"Skipping creation match {match_code} because it already exists.")
                        continue

                    Match.objects.create(
                        code=match_code,
                        competition_in_season=competition_in_season,
                        home_team=home_team,
                        away_team=away_team,
                        date_time=match_datetime,
                        city=home_team.city
                    )
                    match_number += 1

                match_datetime += datetime.timedelta(weeks=1)

            self.stdout.write(self.style.SUCCESS(f'Úspěšně vytvořeny zápasy pro {competition_in_season}'))
