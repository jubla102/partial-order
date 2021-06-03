from django.urls import path

from partial_order import partial_order_detection
from partial_order import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('combinations', views.combinations, name='combinations'),
    path('delays', views.delays, name='delays'),
    path('po-groups', partial_order_detection.get_partial_orders_from_selected_file, name='po-groups'),
    path('final_order', views.final_order, name='final_order')
]
