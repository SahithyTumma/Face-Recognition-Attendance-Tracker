# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    # Auth routes - login / register
    path("", include("apps.authentication.urls")),
    path("", include("apps.home.urls")),
    path("", include("apps.users.urls")),             # UI Kits Html files
]
