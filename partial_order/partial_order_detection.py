import os

from django.http import JsonResponse
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from bootstrapdjango import settings


def get_partial_orders_from_selected_file(request):
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    absolute_file_path = os.path.join(event_logs_path, 'Sepsi_Cases-Event_Log.xes')
    event_log = importer.apply(absolute_file_path)
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    df = df[[CASE_CONCEPT_NAME, DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY]]
    df = df.sort_values(by=['time:timestamp', 'concept:name'])
    partial_order_groups = {'totalNumberOfTraces': len(event_log), 'groups': {}}
    df.groupby(CASE_CONCEPT_NAME).apply(lambda x: check_for_partial_order(x, partial_order_groups))
    df[DEFAULT_TIMESTAMP_KEY] = df[DEFAULT_TIMESTAMP_KEY].astype(str)
    df = df.sort_values(by=[DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY])

    df.groupby(CASE_CONCEPT_NAME).apply(lambda x: check_for_partial_order(x, partial_order_groups))

    return JsonResponse(partial_order_groups, safe=False)


def check_for_partial_order(case, partial_order_groups):
    events = []
    if not case[DEFAULT_TIMESTAMP_KEY].is_unique:
        case.groupby(DEFAULT_TIMESTAMP_KEY).apply(lambda x: append_partial_ordered_events(x, events))
        key = ''.join(events)

        if key in partial_order_groups:
            partial_order_groups['groups'][key]['numberOfCases'] = partial_order_groups[key]['numberOfCases'] + 1
        else:
            partial_order_groups['groups'][key] = {'numberOfCases': 1}
            partial_order_groups['groups'][key]['cases'] = [[*case.to_dict('index').values()]]


def append_partial_ordered_events(x, events):
    events.extend(['|'] + x[DEFAULT_NAME_KEY].values.tolist() + ['|'])
