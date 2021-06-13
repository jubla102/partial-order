import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.template import loader
from pm4py.objects.log.importer.xes import importer

from partial_order import partial_order_detection, combinations_generation
from partial_order.colors import get_colors_from_file
from partial_order.utils import get_form_data

event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
absolute_file_path = os.path.join(event_logs_path, 'Sepsis_Cases-Event_Log.xes')
event_log = importer.apply(absolute_file_path)
number_of_traces = len(event_log)


def groups(request):
    template = loader.get_template('partial_order/groups.html')

    partial_order_ds = partial_order_detection.get_groups_file()
    number_of_groups = len(partial_order_ds['groups'])

    return HttpResponse(
        template.render(
            {'log_name': settings.EVENT_LOG_NAME,
             'groups': partial_order_ds['groups'].values(),
             'numberOfGroups': range(number_of_groups),
             'totalNumberOfTraces': number_of_traces}, request))


def combinations(request):
    template = loader.get_template('partial_order/combinations.html')
    if request.method == 'POST':
        trace = get_form_data(request, 'partialOrder')
        combinations = combinations_generation.get_order_combinations(trace)
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
    return JsonResponse(get_colors_from_file(), safe=False)
