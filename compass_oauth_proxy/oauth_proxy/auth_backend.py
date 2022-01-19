from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import CompassUser

from .compass import CompassSession, CompassAuthException


class CompassBackend(BaseBackend):
    """
    Authenticate against compass
    """

    def authenticate(self, request, username=None, password=None):
        try:
            compass_user = CompassSession(username, password).profile
        except CompassAuthException:
            return None
        try:
            user = CompassUser.objects.get(member_number=compass_user.member_number)
        except CompassUser.DoesNotExist:
            user = CompassUser.from_compass_profile(username, compass_user)
            user.save()
        return user

    def get_user(self, member_number):
        try:
            return CompassUser.objects.get(pk=member_number)
        except CompassUser.DoesNotExist:
            return None
