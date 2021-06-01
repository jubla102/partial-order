from django.urls import path

from partial_order import partial_order_detection
from partial_order import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('combinations', views.combinations, name='combinations'),
    path('delays', views.delays, name='delays'),
    path('test', partial_order_detection.test_data_structure, name='test')
]
