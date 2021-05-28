from django.urls import path

from . import views

urlpatterns = [
    path('/groups', views.partial_order_processing, name='partial_order')
]
