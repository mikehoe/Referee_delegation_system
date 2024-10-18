from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, OneToOneField, CASCADE, CharField
from django.template.defaultfilters import first
from phonenumber_field.modelfields import PhoneNumberField

from referees.models import Referee


class ProfileReferee(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    referee = OneToOneField(Referee, on_delete=CASCADE, related_name='profile')

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"ProfileReferee(username='{self.user.username}' licence={self.referee.licence_number})"

    def __str__(self):
        return f"Profile referee {self.user.first_name} {self.user.last_name} (username='{self.user.username}')"


class ProfileManager(Model):
    MANAGER_TYPES = [
        ('Referee Manager', 'Referee Manager'),
        ('Delegation Manager', 'Delegation Manager'),
        ('Competition Manager', 'Competition Manager'),
        ('Site Manager', 'Site Manager'),
    ]
    manager_type = CharField(max_length=20, null=True, blank=True, choices=MANAGER_TYPES)
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile_manager')
    phone = PhoneNumberField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"ProfileManager(username='{self.user.username}', type={self.manager_type})"

    def __str__(self):
        return f"Profile manager {self.user.first_name} {self.user.last_name} (username='{self.user.username}', type={self.manager_type})"

    def set_permissions(self):
        if self.manager_type == 'Referee Manager':
            self.add_model_permissions('referee', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Delegation Manager':
            self.add_model_permissions('unavailability', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('delegation', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Competition Manager':
            self.add_model_permissions('city', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('season', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('competitioninseason', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('team', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('match', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Site Manager':
            self.add_model_permissions('profilemanager', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('referee', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('unavailability', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('delegation', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('city', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('season', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('competitioninseason', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('team', ['add', 'change', 'delete', 'view'])
            self.add_model_permissions('match', ['add', 'change', 'delete', 'view'])

    def unset_permissions(self):
        if self.manager_type == 'Referee Manager':
            self.remove_model_permissions('referee', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Delegation Manager':
            self.remove_model_permissions('unavailability', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('delegation', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Competition Manager':
            self.remove_model_permissions('city', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('season', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('competitioninseason', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('team', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('match', ['add', 'change', 'delete', 'view'])
        elif self.manager_type == 'Site Manager':
            self.remove_model_permissions('profilemanager', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('referee', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('unavailability', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('delegation', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('city', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('season', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('competitioninseason', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('team', ['add', 'change', 'delete', 'view'])
            self.remove_model_permissions('match', ['add', 'change', 'delete', 'view'])

    def add_model_permissions(self, model_name, actions):
        content_type = ContentType.objects.get(model=''.join(model_name.split('_')))
        for action in actions:
            perm_codename = f'{action}_{model_name}'
            permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
            self.user.user_permissions.add(permission)

    def remove_model_permissions(self, model_name, actions):
        content_type = ContentType.objects.get(model=''.join(model_name.split('_')))
        for action in actions:
            perm_codename = f'{action}_{model_name}'
            permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
            self.user.user_permissions.remove(permission)
