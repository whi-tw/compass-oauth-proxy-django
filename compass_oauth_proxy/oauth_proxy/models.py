from __future__ import annotations
from django.db import models


from django.contrib.auth.models import AbstractUser

from .compass.profile import CompassProfile


class CompassUser(AbstractUser):
    member_number = models.IntegerField(editable=False, unique=True)
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    can_create_oauth_tokens = models.BooleanField(default=False)
    backend = "oauth_proxy.auth_backend.CompassBackend"

    @staticmethod
    def from_compass_profile(username: str, profile: CompassProfile) -> CompassUser:
        user = CompassUser()
        user.username = username
        user.member_number = profile.member_number
        user.email = profile.email
        user.first_name = profile.get_first_name()
        user.last_name = profile.surname
        user.set_unusable_password()
        return user

    def created_from_compass(self):
        if self.member_number > 0:
            return True
        return False
