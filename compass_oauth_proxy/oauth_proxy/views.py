from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import TemplateView

from oauth2_provider import views as oauth2_provider_views

from oauth_proxy.forms import OauthAdminAuthenticationForm

from oauth_proxy.models import User, Groups


class UserIsAppManagerMixin(UserPassesTestMixin):
    def test_func(self):
        is_in_group = self.request.user.groups.filter(
            name=Groups.OAUTH_APP_MANAGERS.name
        ).exists()
        print(is_in_group)
        return is_in_group


class ApplicationList(UserIsAppManagerMixin, oauth2_provider_views.ApplicationList):
    pass


class ApplicationRegistration(
    UserIsAppManagerMixin, oauth2_provider_views.ApplicationRegistration
):
    pass


class ApplicationDetail(UserIsAppManagerMixin, oauth2_provider_views.ApplicationDetail):
    pass


class ApplicationDelete(UserIsAppManagerMixin, oauth2_provider_views.ApplicationDelete):
    pass


class ApplicationUpdate(UserIsAppManagerMixin, oauth2_provider_views.ApplicationUpdate):
    pass


def oauth_management_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("oauth2_management:list")
    form = OauthAdminAuthenticationForm(
        request=request.POST or None, data=request.POST or None
    )
    if request.method == "POST":
        if form.is_valid():
            user: User = form.user_cache
            login(request, user)
            return redirect(form.data.get("next"))
    return render(
        request,
        "registration/oauth_admin_login.html",
        {"form": form, "next": "/oauth/applications"},
    )


def oauth_client_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("/oauth/applications")
    form = OauthAdminAuthenticationForm(
        request=request.POST or None, data=request.POST or None
    )
    next = ""
    if request.method == "POST":
        next = form.data.get("next")
        if form.is_valid():
            user = form.user_cache
            if not user.can_create_oauth_tokens:
                user.can_create_oauth_tokens = True
                user.save()
            login(request, user)
            return redirect(form.data.get("next"))
    elif request.method == "GET":
        next = request.GET.get("next")
    return render(
        request,
        "registration/oauth_client_login.html",
        {"form": form, "next": next},
    )
