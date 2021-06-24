from django.urls import path

from partial_order import partial_order_detection
from partial_order import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
    path('po-groups', partial_order_detection.get_partial_orders_from_selected_file, name='po-groups'),
    path('combinations/<group_id>', views.combinations, name='combinations'),
    path('combinations', views.combinations, name='combinations_error'),
    path('delays/<group_id>/<combination_id>', views.delays, name='delays'),
    path('delays/<group_id>', views.delays, name='delays_without_group'),
    path('delays', views.delays, name='delays_without_group_combination'),
    path('final-order/<group_id>/<combination_id>', views.final_order, name='final_order'),
    path('save-delay', views.save_delay, name='save-delay'),
    path('colors', views.meta_data, name='colors'),
    path('text-widths', views.text_width, name='text-widths'),
    path('download-modified-xes', views.download_modified_xes, name='download')
]
