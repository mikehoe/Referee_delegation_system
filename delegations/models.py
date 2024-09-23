from competitions.models import Match
from referees.models import Referee
from referee_delegation_system.settings import REFEREE_ROLES

from django.db.models import Model, ForeignKey, CASCADE, CharField


class Delegation(Model):
    REFEREE_ROLES = REFEREE_ROLES

    match = ForeignKey(Match, null=False, blank=False, on_delete=CASCADE, related_name='delegated_referees')
    referee = ForeignKey(Referee, null=False, blank=False, on_delete=CASCADE, related_name='delegations')
    referee_role = CharField(max_length=5, null=False, blank=False, choices=REFEREE_ROLES)

    class Meta:
        ordering = ['match__date_time']

    def __repr__(self):
        return f"Delegation(match={self.match}, referee={self.referee}, referee_role={self.referee_role}"

    def __str__(self):
        return f"{self.match}, {self.referee} ({self.referee_role})"

    def notification(self):
        pass
