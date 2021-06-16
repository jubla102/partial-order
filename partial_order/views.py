from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader

from partial_order import partial_order_detection, combinations_generation
from partial_order.general_functions import get_meta_data, get_form_data


def groups(request):
    template = loader.get_template('partial_order/groups.html')

    number_of_groups = 0
    groups = None
    if settings.EVENT_LOG_NAME != ':notset:':
        partial_order_ds = partial_order_detection.get_groups_file()
        number_of_groups = len(partial_order_ds['groups'])
        groups = partial_order_ds['groups'].values()

    return HttpResponse(
        template.render(
            {'log_name': settings.EVENT_LOG_NAME,
             'groups': groups,
             'numberOfGroups': range(number_of_groups),
             'totalNumberOfTraces': settings.NUMBER_OF_TRACES}, request))


def combinations(request):
    template = loader.get_template('partial_order/combinations.html')

    if request.method == 'POST':
        variant = get_form_data(request, 'partialOrder')
        longest_activity_width = get_form_data(request, 'longestActivityWidth')
        text_widths = get_form_data(request, 'textWidths')
        combinations = combinations_generation.get_order_combinations(variant)
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'combinations': combinations, 'longestActivityWidth': longest_activity_width,
                         'textWidths': text_widths, 'totalNumberOfTraces': settings.NUMBER_OF_TRACES}, request))


def delays(request):
    template = loader.get_template('partial_order/delays.html')
    if request.method == 'POST':
        combination = get_form_data(request, 'combination')
        longest_activity_width = get_form_data(request, 'longestActivityWidth')
        text_widths = get_form_data(request, 'textWidths')
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'combination': combination, 'longestActivityWidth': longest_activity_width,
                         'textWidths': text_widths}, request))


def final_order(request):
    template = loader.get_template('partial_order/final_order.html')
    return HttpResponse(template.render({'log_name': settings.EVENT_LOG_NAME}, request))


def meta_data(request):
    return JsonResponse(get_meta_data(), safe=False)


def text_width(request):
    if request.method == 'POST':
        print(request.POST.dict())
        # text_widths = get_form_data(request, 'textWidths')

        return HttpResponse()
    else:
        return HttpResponseNotFound()
