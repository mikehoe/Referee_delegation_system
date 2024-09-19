from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, CharField
#from referees.models import Referee

class ProfileReferee(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    referee = OneToOneField(Referee, on_delete=CASCADE)

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"Profile (user = '{self.user.username})'"

    def __str__(self):
        return f"Profile (user = '{self.user.username})'"


class ProfileManager(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    phone = CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"Profile (user = '{self.user.username})'"

    def __str__(self):
        return f"Profile (user = '{self.user.username})'"