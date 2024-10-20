from django.core.exceptions import ValidationError

from competitions.models import Match
from referees.models import Referee

from django.db.models import Model, ForeignKey, CASCADE, CharField, TextChoices


class RefereeRole(TextChoices):
    FIRST_REFEREE = '1.R', '1st referee'
    SECOND_REFEREE = '2.R', '2nd referee'
    FIRST_LINE_JUDGE = '1.L', '1st line judge'
    SECOND_LINE_JUDGE = '2.L', '2nd line judge'


class Delegation(Model):
    match = ForeignKey(Match, null=False, blank=False, on_delete=CASCADE, related_name='delegated_referees')
    referee = ForeignKey(Referee, null=False, blank=False, on_delete=CASCADE, related_name='delegations')
    referee_role = CharField(max_length=3, null=False, blank=False, choices=RefereeRole.choices)

    class Meta:
        ordering = ['match__date_time']

        # Ensuring that a referee cannot be delegated to the same role more than once for the same match
        unique_together = ('match', 'referee')

    def __repr__(self):
        return (f"Delegation(match={self.match.code}, referee={self.referee.name} {self.referee.surname}, "
                f"referee_role={self.referee_role})")

    def __str__(self):
        return f"{self.match.code}, {self.referee.name} {self.referee.surname}, ({self.referee_role})"

    # Filtering and returning referees who are qualified, available
    # and not already delegated to another match at the same day
    @staticmethod
    def get_available_referees(match, referee_role):

        # Filtering referees which are qualified for match
        from referees.models import Referee

        if referee_role in {RefereeRole.FIRST_REFEREE, RefereeRole.SECOND_REFEREE}:
            # 1st referee or 2nd referee are qualified by licence

            if match.competition_in_season.competition.level_id == 1:
                qualified_referees = Referee.objects.filter(
                    licence_type__competition_levels=match.competition_in_season.competition.level
                ).order_by('-rating', '-licence_type')  # At the highest competition level, prioritize the rating
            else:
                qualified_referees = Referee.objects.filter(
                    licence_type__competition_levels=match.competition_in_season.competition.level
                ).order_by('-licence_type', '-rating')
        else:
            # As line judge can be qualified all
            qualified_referees = Referee.objects.all().order_by('-licence_type', '-rating')

        # Filtering referees who are qualified and available
        from referees.models import Unavailability
        unavailable_referees = Unavailability.objects.filter(
            date_from__lte=match.date_time.date(),
            date_to__gte=match.date_time.date()
        ).values_list('referee', flat=True)  # Just IDs list
        available_qualified_referees = qualified_referees.exclude(id__in=unavailable_referees)

        # Filtering and returning referees who are qualified, available
        # and not already delegated to another match at the same day
        delegated_referees_to_another_match_same_day = Delegation.objects.filter(
            match__date_time__date=match.date_time.date()
        ).exclude(match=match).values_list('referee', flat=True)  # Just IDs list
        return available_qualified_referees.exclude(id__in=delegated_referees_to_another_match_same_day)

    # TODO: Send email notification to delegate referees
    def notification(self):
        pass
