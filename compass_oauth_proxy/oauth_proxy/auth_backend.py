from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Group
from .models import User

from .compass import CompassSession, CompassAuthException


class CompassBackend(BaseBackend):
    """
    Authenticate against compass
    """

    def authenticate(self, request, username=None, password=None):
        try:
            compass_user = CompassSession(username, password).profile_data
        except CompassAuthException:
            return None
        try:
            user = User.objects.get(compass_profile__pk=compass_user.member_number)
        except User.DoesNotExist:
            user: User = User(compass_data=compass_user, username=username)
            user.groups.add(Group.objects.get(name="CompassUsers"))
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
