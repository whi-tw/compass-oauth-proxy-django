from typing import Any, Text
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _


class BootstrapTextInput(TextInput):
    template_name = "widgets/input.html"


class BootstrapPasswordInput(PasswordInput):
    template_name = "widgets/input.html"


class OauthAdminAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=BootstrapTextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=BootstrapPasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields are case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }
