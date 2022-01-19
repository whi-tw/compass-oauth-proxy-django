"""compass_oauth_proxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from distutils.log import Log
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from oauth_proxy import views as oauth_proxy_views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # path(
    #     "accounts/login/",
    #     oauth_proxy_views.oauth_client_login,
    #     name="oauth_client_login",
    # ),
    path("accounts/", include("django.contrib.auth.urls"), name="accounts"),
    path(
        "oauth/admin_login",
        oauth_proxy_views.oauth_management_login,
        name="oauth_mgmt_login",
    ),
    path(
        "oauth/admin_logout",
        LogoutView.as_view(next_page="/oauth/admin_login"),
        name="oauth_mgmt_logout",
    ),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path(
        "",
        RedirectView.as_view(url="/oauth/admin_login", permanent=True),
        name="oauth_mgmt_home",
    ),
]
