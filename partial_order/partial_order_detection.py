import json
import os

from django.http import JsonResponse
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from bootstrapdjango import settings
from partial_order.colors import get_colors, get_colors_from_file


def get_partial_orders_from_selected_file(request):
    partial_order_groups = get_groups_file()

    return JsonResponse(partial_order_groups, safe=False)


def get_groups_file():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    # absolute_file_path = os.path.join(event_logs_path, 'simple-test.xes')
    absolute_file_path = os.path.join(event_logs_path, 'Sepsis_Cases-Event_Log.xes')
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp")
    temp_groups_file = os.path.join(temp_path, 'partial_orders_Sepsis_Cases-Event_Log.json')
    temp_color_file = os.path.join(temp_path, 'colors_Sepsis_Cases-Event_Log.json')
    if os.path.exists(temp_groups_file):
        with open(temp_groups_file) as groups_file:
            partial_order_groups = json.load(groups_file)

        partial_order_groups['colors'] = get_colors_from_file()
    else:
        event_log = importer.apply(absolute_file_path)
        df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
        df[DEFAULT_TIMESTAMP_KEY] = df[DEFAULT_TIMESTAMP_KEY].astype(str)
        activities = df[DEFAULT_NAME_KEY].unique().tolist()
        partial_order_groups = {'totalNumberOfTraces': len(event_log), 'groups': get_partial_order_groups(df)}
        colors = get_colors(activities)
        with open(temp_groups_file, 'w') as outfile_groups, open(temp_color_file, 'w') as outfile_colors:
            json.dump(partial_order_groups, outfile_groups, indent=4)
            json.dump(colors, outfile_colors, indent=4)

    return partial_order_groups


def get_partial_order_groups(df):
    df = df[[CASE_CONCEPT_NAME, DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY]]
    df = df.sort_values(by=[CASE_CONCEPT_NAME, DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY])
    groups = {}
    df.groupby(CASE_CONCEPT_NAME).apply(lambda x: check_for_partial_order(x, groups))

    return groups


def check_for_partial_order(case, partial_order_groups):
    events = []
    if not case[DEFAULT_TIMESTAMP_KEY].is_unique:
        case.groupby(DEFAULT_TIMESTAMP_KEY).apply(lambda x: create_group_hash_list(x, events))
        key = ''.join(events)

        case_id = case[CASE_CONCEPT_NAME][0]
        if key in partial_order_groups:
            partial_order_groups[key]['caseIds'].append(case_id)

            partial_order_groups[key]['numberOfCases'] = partial_order_groups[key][
                                                             'numberOfCases'] + 1
        else:
            partial_order_groups[key] = {'numberOfCases': 1}
            partial_order_groups[key]['caseIds'] = [case_id]
            partial_order_groups[key]['events'] = [*case.to_dict('index').values()]


def create_group_hash_list(x, events):
    events.extend(['|'] + x[DEFAULT_NAME_KEY].values.tolist() + ['|'])
