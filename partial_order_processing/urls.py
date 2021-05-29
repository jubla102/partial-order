from django.urls import path

from . import views

urlpatterns = [
    path('/groups', views.partial_order_processing, name='partial_order_processing'),
    path('/delay', views.add_delays, name='add_delays')
]
