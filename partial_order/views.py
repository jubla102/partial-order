import json
import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader

from partial_order import partial_order_detection, combinations_generation
from partial_order.general_functions import get_meta_data, get_form_data, get_group_from_file, get_export_file_path
from partial_order.save_delays_to_log import save_delay_to_log


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
        delay = get_form_data(request, 'delay')
    else:
        return HttpResponseNotFound()

    return HttpResponse(
        template.render({'groupId': groupId,
                         'combination': combination,
                         'caseIds': caseIds,
                         'delay': delay}, request))


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
