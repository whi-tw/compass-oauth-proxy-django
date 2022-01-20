from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from .models import User, CompassProfile

from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "from_compass",
        "get_membership_number",
        "is_staff",
    )
    list_filter = BaseUserAdmin.list_filter

    @admin.display(boolean=True)
    def from_compass(self, user: User) -> Optional[CompassProfile]:
        return user.compass_profile is not None

    @admin.display(description="Membership Number", empty_value="-")
    def get_membership_number(self, user: User) -> Union[int, str]:
        return user.compass_profile.member_number if user.compass_profile else None
