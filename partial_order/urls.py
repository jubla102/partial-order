from django.urls import path

from partial_order import partial_order_detection
from partial_order import views

urlpatterns = [
    # views for happy path
    path('groups', views.groups, name='groups'),
    path('po-groups', partial_order_detection.get_partial_orders_from_selected_file, name='po-groups'),
    path('combinations/<group_id>', views.combinations, name='combinations'),
    path('delays/<group_id>/<combination_id>', views.delays, name='delays'),
    path('save-and-export/<group_id>/<combination_id>', views.save_and_export, name='save_and_export'),

    # api
    path('save-delay', views.save_delay, name='save-delay'),
    path('metadata', views.meta_data, name='metadata'),
    path('text-widths', views.text_width, name='text-widths'),
    path('download-modified-xes', views.download_modified_xes, name='download'),

    # the following urls are just used to differentiate between errors
    path('combinations', views.combinations, name='combinations_error'),
    path('delays/<group_id>', views.delays, name='delays_without_group'),
    path('delays', views.delays, name='delays_without_group_combination'),
    path('save-and-export/<group_id>', views.save_and_export, name='save_and_export_with_group'),
    path('save-and-export', views.save_and_export, name='save_and_export_error')
]
