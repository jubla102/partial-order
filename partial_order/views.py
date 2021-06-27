import json
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader

from partial_order import partial_order_detection, combinations_generation
from partial_order.general_functions import get_meta_data, get_export_file_path
from partial_order.save_delays_to_log import save_delay_to_log


def groups(request):
    template = loader.get_template('partial_order/groups.html')

    number_of_groups = 0
    groups = None
    if settings.EVENT_LOG_NAME != ':notset:':
        partial_order_ds = partial_order_detection.get_groups_file()
        number_of_groups = len(partial_order_ds['groups'])
        groups = list(partial_order_ds['groups'].values())

    groups.sort(key=lambda x: x['numberOfCases'], reverse=True)

    return HttpResponse(
        template.render(
            {'log_name': settings.EVENT_LOG_NAME,
             'groups': groups,
             'numberOfGroups': range(number_of_groups),
             'totalNumberOfTraces': settings.NUMBER_OF_TRACES}, request))


def combinations(request, group_id=None):
    template = loader.get_template('partial_order/combinations.html')

    if group_id is None:
        combinations = None
        case_ids = None
    else:
        group = settings.GROUPS['groups'][group_id]
        combinations = combinations_generation.get_order_combinations(group['events'])
        case_ids = group['caseIds']

    return HttpResponse(
        template.render(
            {'groupId': group_id,
             'combinations': combinations,
             'caseIds': case_ids,
             'totalNumberOfTraces': settings.NUMBER_OF_TRACES},
            request))


def delays(request, group_id=None, combination_id=None):
    template = loader.get_template('partial_order/delays.html')

    if group_id is None or combination_id is None:
        combination = None
        case_ids = None
    else:
        group = settings.GROUPS['groups'][group_id]
        combination = combinations_generation.get_order_combinations(group['events'])[int(combination_id)]['events']
        case_ids = group['caseIds']

    return HttpResponse(
        template.render({'groupId': group_id,
                         'combinationId': combination_id,
                         'combination': combination,
                         'caseIds': case_ids}, request))


def final_order(request, group_id=None, combination_id=None):
    template = loader.get_template('partial_order/final_order.html')

    if group_id is None or combination_id is None:
        combination = None
        case_ids = None
        delay = None
    else:
        group = settings.GROUPS['groups'][group_id]
        combination = combinations_generation.get_order_combinations(group['events'])[int(combination_id)]['events']
        case_ids = group['caseIds']
        delay = request.GET.get('delay')

    return HttpResponse(
        template.render({'groupId': group_id,
                         'combinationId': combination_id,
                         'combination': combination,
                         'caseIds': case_ids,
                         'delay': int(delay)}, request))


def meta_data(request):
    return JsonResponse(get_meta_data(), safe=False)


def text_width(request):
    if request.method == 'POST':
        text_widths = json.loads(request.body.decode('utf-8'))['textWidths']
        settings.TEXT_WIDTHS = text_widths

        return HttpResponse()
    else:
        return HttpResponseNotFound()


def save_delay(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        groupId = json.loads(request_body['groupId'])
        caseIds = json.loads(request_body['caseIds'])
        events = json.loads(request_body['events'])
        delay = request_body['delay']

        variant_obj = {"group": groupId, "delay": delay, "caseIds": caseIds,
                       "events": events}
        save_delay_to_log(variant_obj)

        return HttpResponse()
    else:
        return HttpResponseNotFound()


def download_modified_xes(request):
    try:
        file = get_export_file_path()
        wrapper = FileWrapper(open(file, 'rb'))
        response = HttpResponse(wrapper, content_type='application/force-download')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)

        return response
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
