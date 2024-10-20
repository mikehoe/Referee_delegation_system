from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField

from competitions.models import Match
from delegations.models import Delegation, RefereeRole
from referees.models import Referee


class MatchDelegationForm(forms.Form):
    referee_1R = forms.ModelChoiceField(
        queryset=Referee.objects.none(),
        required=False,
        label='1.R'
    )
    referee_2R = forms.ModelChoiceField(
        queryset=Referee.objects.none(),
        required=False,
        label='2.R'
    )
    referee_1L = forms.ModelChoiceField(
        queryset=Referee.objects.none(),
        required=False,
        label='1.L'
    )
    referee_2L = forms.ModelChoiceField(
        queryset=Referee.objects.none(),
        required=False,
        label='2.L'
    )

    def set_default_referee_names(self, match):
        delegations = Delegation.objects.filter(match=match)
        for delegation in delegations:
            if delegation.referee_role == RefereeRole.FIRST_REFEREE:
                self.fields['referee_1R'].initial = delegation.referee
            elif delegation.referee_role == RefereeRole.SECOND_REFEREE:
                self.fields['referee_2R'].initial = delegation.referee
            elif delegation.referee_role == RefereeRole.FIRST_LINE_JUDGE:
                self.fields['referee_1L'].initial = delegation.referee
            elif delegation.referee_role == RefereeRole.SECOND_LINE_JUDGE:
                self.fields['referee_2L'].initial = delegation.referee

    def __init__(self, *args, match=None, **kwargs):
        super().__init__(*args, **kwargs)

        if match:
            self.set_default_referee_names(match)

            self.fields['referee_1R'].queryset = Delegation.get_available_referees(match, RefereeRole.FIRST_REFEREE)
            self.fields['referee_2R'].queryset = Delegation.get_available_referees(match, RefereeRole.SECOND_REFEREE)
            self.fields['referee_1L'].queryset = Delegation.get_available_referees(match, RefereeRole.FIRST_LINE_JUDGE)
            self.fields['referee_2L'].queryset = Delegation.get_available_referees(match, RefereeRole.SECOND_LINE_JUDGE)

            delegations = Delegation.objects.filter(match=match)
            for delegation in delegations:
                if delegation.referee_role == RefereeRole.FIRST_REFEREE:
                    self.fields['referee_1R'].initial = delegation.referee
                elif delegation.referee_role == RefereeRole.SECOND_REFEREE:
                    self.fields['referee_2R'].initial = delegation.referee
                elif delegation.referee_role == RefereeRole.FIRST_LINE_JUDGE:
                    self.fields['referee_1L'].initial = delegation.referee
                elif delegation.referee_role == RefereeRole.SECOND_LINE_JUDGE:
                    self.fields['referee_2L'].initial = delegation.referee

    def clean(self):
        cleaned_data = super().clean()
        match_id = self.data.get('match_id')

        for role in ['1.R', '2.R', '1.L', '2.L']:
            referee = cleaned_data.get(f'referee_{role}')
            if referee:
                if Delegation.objects.filter(match_id=match_id, referee=referee).exists():
                    raise ValidationError(f"Referee {referee} is already delegated to this match.")

                match = Match.objects.get(id=match_id)
                if Delegation.objects.filter(match__date_time__date=match.date_time.date(), referee=referee).exists():
                    raise ValidationError(
                        f"Referee {referee} is already delegated on {match.date_time.date()} for another match.")

    def save(self, match):
        referees = {
            '1.R': self.cleaned_data.get('referee_1R'),
            '2.R': self.cleaned_data.get('referee_2R'),
            '1.L': self.cleaned_data.get('referee_1L'),
            '2.L': self.cleaned_data.get('referee_2L'),
        }

        for role, referee in referees.items():
            if referee is not None:
                # Trying to find existing delegation
                existing_delegation = Delegation.objects.filter(match=match, referee_role=role).first()
                if existing_delegation:
                    # If exists, update it
                    existing_delegation.referee = referee
                    existing_delegation.save()
                else:
                    # If doesn’t exist, create new
                    Delegation.objects.create(match=match, referee_role=role, referee=referee)
            else:
                # If referee is None ('----'), delete delegation
                Delegation.objects.filter(match=match, referee_role=role).delete()


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
