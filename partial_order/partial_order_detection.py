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
    absolute_file_path = os.path.join(event_logs_path, settings.EVENT_LOG_NAME)
    event_log = importer.apply(absolute_file_path)
    partial_order_groups = get_partial_order_groups(event_log)

    return JsonResponse(partial_order_groups, safe=False)


def get_partial_order_groups(event_log):
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    df = df[[CASE_CONCEPT_NAME, DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY]]
    df = df.sort_values(by=[CASE_CONCEPT_NAME, DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY])
    partial_order_groups = {'totalNumberOfTraces': len(event_log), 'groups': {}}
    df.groupby(CASE_CONCEPT_NAME).apply(lambda x: check_for_partial_order(x, partial_order_groups))
    df[DEFAULT_TIMESTAMP_KEY] = df[DEFAULT_TIMESTAMP_KEY].astype(str)

    return partial_order_groups


def check_for_partial_order(case, partial_order_groups):
    events = []
    if not case[DEFAULT_TIMESTAMP_KEY].is_unique:
        case.groupby(DEFAULT_TIMESTAMP_KEY).apply(lambda x: create_group_hash_list(x, events))
        key = ''.join(events)

        if key in partial_order_groups['groups']:
            partial_order_groups['groups'][key]['numberOfCases'] = partial_order_groups['groups'][key][
                                                                       'numberOfCases'] + 1
        else:
            partial_order_groups['groups'][key] = {'numberOfCases': 1}
            partial_order_groups['groups'][key]['events'] = [*case.to_dict('index').values()]


def create_group_hash_list(x, events):
    events.extend(['|'] + x[DEFAULT_NAME_KEY].values.tolist() + ['|'])


if __name__ == '__main__':
    print(get_partial_orders_from_selected_file(None))
