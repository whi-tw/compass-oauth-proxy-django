from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpRequest

from oauth_proxy.forms import OauthAdminAuthenticationForm


def oauth_management_login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("/oauth/applications")
    form = OauthAdminAuthenticationForm(
        request=request.POST or None, data=request.POST or None
    )
    if request.method == "POST":
        if form.is_valid():
            user = form.user_cache
            if not user.can_create_oauth_tokens:
                user.can_create_oauth_tokens = True
                user.save()
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
