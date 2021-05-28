from django.urls import path

from . import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('combinations', views.combinations, name='combinations'),
    path('delays', views.delays, name='delays')
]
