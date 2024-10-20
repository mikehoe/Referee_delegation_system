from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField

from competitions.models import Match
from delegations.models import Delegation, RefereeRole
from referees.models import Referee


class BulkDelegationForm(forms.Form):
    hidden = forms.ModelMultipleChoiceField(
        queryset=Match.objects.none(), widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        matches = kwargs.pop('matches')
        super().__init__(*args, **kwargs)

        if matches:
            # Dynamicky generujeme pole pro každou roli (1.R, 2.R, 1.L, 2.L) pro každý zápas
            for match in matches:
                for role in ['1R', '2R', '1L', '2L']:
                    self.fields[f'referee_{match.id}_{role}'] = forms.ModelChoiceField(
                        queryset=Delegation.get_available_referees(match, RefereeRole.FIRST_REFEREE),
                        required=False,
                        label=f'1.R for {match}'
                    )
                    self.fields[f'referee_{match.id}_{role}'] = forms.ModelChoiceField(
                        queryset=Delegation.get_available_referees(match, RefereeRole.SECOND_REFEREE),
                        required=False,
                        label=f'2.R for {match}'
                    )
                    self.fields[f'referee_{match.id}_{role}'] = forms.ModelChoiceField(
                        queryset=Delegation.get_available_referees(match, RefereeRole.FIRST_LINE_JUDGE),
                        required=False,
                        label=f'1.L for {match}'
                    )
                    self.fields[f'referee_{match.id}_{role}'] = forms.ModelChoiceField(
                        queryset=Delegation.get_available_referees(match, RefereeRole.SECOND_LINE_JUDGE),
                        required=False,
                        label=f'2.L for {match}'
                    )

    def clean(self):
        cleaned_data = super().clean()

        for field_name, referee in cleaned_data.items():
            if referee:
                # Validace - kontrola, zda rozhodčí není přiřazen vícekrát ke stejnému zápasu
                match_id = field_name.split('_')[1]
                role = field_name.split('_')[2]
                if Delegation.objects.filter(match_id=match_id, referee=referee).exists():
                    raise ValidationError(f"Referee {referee} is already delegated to this match.")

                # Validace - kontrola, zda rozhodčí není přiřazen k jiným zápasům ve stejný den
                match = Match.objects.get(id=match_id)
                if Delegation.objects.filter(match__date_time__date=match.date_time.date(),
                                             referee=referee).exists():
                    raise ValidationError(
                        f"Referee {referee} is already delegated on {match.date_time.date()} for another match.")
