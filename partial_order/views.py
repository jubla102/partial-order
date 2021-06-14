from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader

from partial_order import partial_order_detection, combinations_generation, general_functions
from partial_order.general_functions import get_metadata_from_file
from partial_order.utils import get_form_data


def groups(request):
    template = loader.get_template('partial_order/groups.html')

    number_of_groups = 0
    number_of_traces = 0
    groups = None
    if settings.EVENT_LOG_NAME != ':notset:':
        number_of_traces = general_functions.get_number_of_traces()
        partial_order_ds = partial_order_detection.get_groups_file()
        number_of_groups = len(partial_order_ds['groups'])
        groups = partial_order_ds['groups'].values()

    return HttpResponse(
        template.render(
            {'log_name': settings.EVENT_LOG_NAME,
             'groups': groups,
             'numberOfGroups': range(number_of_groups),
             'totalNumberOfTraces': number_of_traces}, request))


def combinations(request):
    template = loader.get_template('partial_order/combinations.html')

    number_of_traces = general_functions.get_number_of_traces()
    if request.method == 'POST':
        variant = get_form_data(request, 'partialOrder')
        combinations = combinations_generation.get_order_combinations(variant)
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'combinations': combinations, 'totalNumberOfTraces': number_of_traces}, request))


def delays(request):
    template = loader.get_template('partial_order/delays.html')
    if request.method == 'POST':
        combination = get_form_data(request, 'combination')
    else:
        return HttpResponseNotFound()

    return HttpResponse(template.render({'combination': combination}, request))


def final_order(request):
    template = loader.get_template('partial_order/final_order.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def colors(request):
    return JsonResponse(get_metadata_from_file(), safe=False)
