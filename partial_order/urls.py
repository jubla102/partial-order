from django.urls import path

from partial_order import partial_order_detection
from partial_order import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('po-groups', partial_order_detection.get_partial_orders_from_selected_file, name='po-groups'),
    path('combinations/<group_id>', views.combinations, name='combinations'),
    path('delays', views.delays, name='delays'),
    path('save-and-export', views.save_and_export, name='save_and_export'),
    path('save-delay', views.save_delay, name='save-delay'),
    path('colors', views.meta_data, name='colors'),
    path('text-widths', views.text_width, name='text-widths'),
    path('download-modified-xes', views.download_modified_xes, name='download')
]
