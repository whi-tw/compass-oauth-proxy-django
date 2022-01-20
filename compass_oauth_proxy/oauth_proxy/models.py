from __future__ import annotations
from typing import Optional, Union
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType

from oauth_proxy.compass import CompassProfileData


class Groups:
    COMPASS_USERS, _ = Group.objects.get_or_create(name="Compass Users")
    OAUTH_USERS, _ = Group.objects.get_or_create(name="OAuth Users")
    OAUTH_APP_MANAGERS, _ = Group.objects.get_or_create(name="Oauth App Managers")

    @classmethod
    def setup_group_permissions(cls):
        oauth2_application_ct = ContentType.objects.get(
            app_label="oauth2_provider", model="application"
        )
        perms = Permission.objects.filter(
            content_type=oauth2_application_ct, codename__endswith="application"
        )
        cls.OAUTH_APP_MANAGERS.permissions.set(perms)


class CompassProfile(models.Model):
    member_number = models.IntegerField(primary_key=True)
    join_date = models.DateField(verbose_name="Date joined scouting")


class User(AbstractUser):
    email = models.EmailField()
    known_as = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    compass_profile = models.ForeignKey(
        CompassProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __init__(
        self, *args, compass_data: CompassProfileData = None, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if compass_data:
            self.populate_from_compass(compass_data)

    def get_full_name(self) -> str:
        return f"{self.get_short_name()} {self.last_name}"

    def get_short_name(self) -> str:
        return self.known_as if self.known_as else self.first_name.split(" ")[0]

    def get_compass_member_number(self) -> Optional[int]:
        return self.compass_profile.member_number if self.compass_profile else None

    def populate_from_compass(self, profile_data: CompassProfileData):
        self.email = profile_data.email
        self.first_name = profile_data.forename
        self.last_name = profile_data.surname
        self.known_as = profile_data.known_as
        self.compass_profile = CompassProfile()
        self.compass_profile.member_number = profile_data.member_number
        self.compass_profile.join_date = profile_data.join_date
        self.compass_profile.save()
        self.save()
