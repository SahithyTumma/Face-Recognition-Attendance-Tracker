# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from apps.users import views
from .views import register_user
urlpatterns = [
    path('main', views.index, name='main'),
    path('register_user', register_user, name="register_user"),
    path('map', views.map, name="map"),
    path('profile', views.profile, name="profile"),
    path('Maintables', views.Maintables, name="Maintables"),
    path('get_name', views.get_name, name="get_name"),
    path('filter', views.filter, name="filter"),
    path('delete', views.delete, name="delete"),
]
