from django.conf import settings
from django.http import JsonResponse
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from partial_order.general_functions import get_selected_file_path


def get_partial_orders_from_selected_file(request):
    partial_order_groups = get_groups_file()

    return JsonResponse(partial_order_groups, safe=False)


def get_groups_file():
    if len(settings.GROUPS) != 0:
        partial_order_groups = settings.GROUPS

        partial_order_groups['metadata']['colors'] = settings.COLORS
        partial_order_groups['metadata']['longestActivityName'] = settings.LONGEST_ACTIVITY_NAME
        partial_order_groups['metadata']['textWidths'] = settings.TEXT_WIDTHS
    else:
        event_log = importer.apply(get_selected_file_path())
        df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
        df[DEFAULT_TIMESTAMP_KEY] = df[DEFAULT_TIMESTAMP_KEY].astype(str)
        partial_order_groups = {'groups': get_partial_order_groups(df),
                                'metadata': {
                                    'longestActivityName': settings.LONGEST_ACTIVITY_NAME,
                                    'colors': settings.COLORS,
                                }}

        settings.GROUPS = partial_order_groups

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
