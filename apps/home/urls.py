# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('attendance', views.home, name='attendance'),
    path('', views.main, name="main"),
    path('home', views.index, name='home'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('recognize', views.recognize, name='recognize'),
    path('capture', views.capture, name='capture'),
    path('add', views.add, name="add"),
    path('homeprofile', views.homeprofile, name="homeprofile"),
    path('tables', views.tables, name="tables"),
    path('passwordchange', views.passwordchange, name="passwordchange"),
    path('filters', views.filters, name="filters"),
]
