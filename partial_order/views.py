import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader

from partial_order import partial_order_detection, combinations_generation
from partial_order.general_functions import get_meta_data, get_form_data, get_group_from_file


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


def combinations(request, group_id):
    template = loader.get_template('partial_order/combinations.html')
    group = get_group_from_file(group_id)
    combinations = combinations_generation.get_order_combinations(group['events'])
    case_ids = group['caseIds']

    return HttpResponse(
        template.render(
            {'groupId': group_id,
             'combinations': combinations,
             'caseIds': case_ids,
             'totalNumberOfTraces': settings.NUMBER_OF_TRACES},
            request))


def delays(request):
    template = loader.get_template('partial_order/delays.html')
    if request.method == 'POST':
        groupId = get_form_data(request, 'groupId')
        combination = get_form_data(request, 'combination')
        caseIds = get_form_data(request, 'caseIds')
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'groupId': groupId,
                         'combination': combination,
                         'caseIds': caseIds}, request))


def final_order(request):
    template = loader.get_template('partial_order/final_order.html')
    if request.method == 'POST':
        groupId = get_form_data(request, 'groupId')
        combination = get_form_data(request, 'combination')
        caseIds = get_form_data(request, 'caseIds')
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'groupId': groupId,
                         'combination': combination,
                         'caseIds': caseIds}, request))


def meta_data(request):
    return JsonResponse(get_meta_data(), safe=False)


def text_width(request):
    if request.method == 'POST':
        text_widths = json.loads(request.body.decode('utf-8'))['textWidths']
        settings.TEXT_WIDTHS = text_widths

        return HttpResponse()
    else:
        return HttpResponseNotFound()
