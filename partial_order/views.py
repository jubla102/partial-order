from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from partial_order import partial_order_detection


def groups(request):
    template = loader.get_template('partial_order/groups.html')

    partial_order_groups = partial_order_detection.get_groups_file()
    number_of_groups = len(partial_order_groups['groups'])

    return HttpResponse(
        template.render({'log_name': settings.EVENT_LOG_NAME, 'numberOfGroups': range(number_of_groups)}, request))


def combinations(request):
    template = loader.get_template('partial_order/combinations.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def delays(request):
    template = loader.get_template('partial_order/delays.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def final_order(request):
    template = loader.get_template('partial_order/final_order.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))
