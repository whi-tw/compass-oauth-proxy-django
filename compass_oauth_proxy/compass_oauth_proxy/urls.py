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
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth.views import LogoutView
import oauth2_provider.views as oauth2_views
import oauth2_provider.urls as oauth2_urls

from oauth_proxy import views as oauth_proxy_views


oauth2_app_management_views = [
    path(
        "applications/",
        oauth_proxy_views.ApplicationList.as_view(),
        name="list",
    ),
    path(
        "applications/register/",
        oauth_proxy_views.ApplicationRegistration.as_view(),
        name="register",
    ),
    path(
        "applications/<pk>/",
        oauth_proxy_views.ApplicationDetail.as_view(),
        name="detail",
    ),
    path(
        "applications/<pk>/delete/",
        oauth_proxy_views.ApplicationDelete.as_view(),
        name="delete",
    ),
    path(
        "applications/<pk>/update/",
        oauth_proxy_views.ApplicationUpdate.as_view(),
        name="update",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="/"),
        name="logout",
    ),
    path(
        "login/",
        oauth_proxy_views.oauth_management_login,
        name="login",
    ),
    path(
        "",
        RedirectView.as_view(url="applications", permanent=True),
        name="oauth_mgmt_home",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # path(
    #     "accounts/login/",
    #     oauth_proxy_views.oauth_client_login,
    #     name="oauth_client_login",
    # ),
    path("accounts/", include("django.contrib.auth.urls"), name="accounts"),
    path(
        "",
        include(
            (
                oauth2_urls.base_urlpatterns + oauth2_urls.oidc_urlpatterns,
                "oauth2_provider",
            ),
            namespace="oauth2_endpoint",
        ),
    ),
    path(
        "app-management/",
        include(
            (oauth2_app_management_views, "oauth2_provider"),
            "oauth2_management",
        ),
        name="oauth_mgmt",
    ),
]
