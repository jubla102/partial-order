import json
import os

from django.http import JsonResponse
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from bootstrapdjango import settings


def test_data_structure(request):
    ds = {
        "colorMap": {
            "ER Registr.": "#EE6352",
            "ER Triage": "#59CD90",
            "Leucocytes": "#3FA7D6",
            "CRP": "#FAC05E",
            "IV Antibiotics": "#F79D84",
            "Release A": "#53A548",
            "Lactic Acid": "#804E49",
            "IV Liquid": "#A69CAC",
            "Admission NC": "#BAF2D8",
            "Return ER": "#9F2042",
            "ER Sepsis": "#788585",
            "l": "#478978",
            "m": "#FA7921",
            "n": "#5BC0EB"
        },
        "groups": [
            {
                "groupId": 1,
                "numerOfCases": 2,
                "percentage": 0.21,
                "cases": [
                    {
                        "caseId": 1,
                        "events": [
                            {
                                "activity": "ER Registr.",
                                "timestamp": "2021-05-11 12:00"
                            },
                            {
                                "activity": "ER Triage",
                                "timestamp": "2021-05-11 12:00"
                            },
                            {
                                "activity": "Leucocytes",
                                "timestamp": "2021-05-11 12:00"
                            }
                        ]
                    }
                ]
            },
            {
                "groupId": 2,
                "numerOfCases": 1,
                "percentage": 0.1,
                "cases": [
                    {
                        "caseId": 1,
                        "events": [
                            {
                                "activity": "ER Registr.",
                                "timestamp": "2021-05-11 12:01"
                            },
                            {
                                "activity": "CRP",
                                "timestamp": "2021-05-11 12:02"
                            },
                            {
                                "activity": "ER Triage",
                                "timestamp": "2021-05-11 12:03"
                            },
                            {
                                "activity": "Leucocytes",
                                "timestamp": "2021-05-11 12:04"
                            },
                            {
                                "activity": "IV Liquid",
                                "timestamp": "2021-05-11 12:05"
                            },
                            {
                                "activity": "Lactic Acid",
                                "timestamp": "2021-05-11 12:06"
                            },
                            {
                                "activity": "IV Liquid",
                                "timestamp": "2021-05-11 12:06"
                            },
                            {
                                "activity": "ER Sepsis",
                                "timestamp": "2021-05-11 12:06"
                            },
                            {
                                "activity": "Release A",
                                "timestamp": "2021-05-11 12:06"
                            },
                            {
                                "activity": "CRP",
                                "timestamp": "2021-05-11 12:07"
                            },
                        ]
                    }
                ]
            },
            {
                "groupId": 2,
                "numerOfCases": 1,
                "percentage": 0.1,
                "cases": [
                    {
                        "caseId": 1,
                        "events": [
                            {
                                "activity": "ER Registr.",
                                "timestamp": "2021-05-11 12:01"
                            },
                            {
                                "activity": "Admission NC",
                                "timestamp": "2021-05-11 12:02"
                            },
                            {
                                "activity": "Return ER",
                                "timestamp": "2021-05-11 12:03"
                            },
                            {
                                "activity": "Lactic Acid",
                                "timestamp": "2021-05-11 12:03"
                            },
                            {
                                "activity": "IV Liquid",
                                "timestamp": "2021-05-11 12:03"
                            },
                            {
                                "activity": "Release A",
                                "timestamp": "2021-05-11 12:04"
                            },
                            {
                                "activity": "Leucocytes",
                                "timestamp": "2021-05-11 12:04"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return JsonResponse(ds, safe=False)


def get_partial_orders_from_selected_file(request):
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    absolute_file_path = os.path.join(event_logs_path, 'Sepsis_Cases-Event_Log.xes')

    temp_path = os.path.join(settings.MEDIA_ROOT, "temp")
    temp_file = os.path.join(temp_path, 'partial_orders_Sepsis_Cases-Event_Log.json')
    if os.path.exists(temp_file):
        with open(temp_file) as json_file:
            partial_order_groups = json.load(json_file)
    else:
        event_log = importer.apply(absolute_file_path)
        partial_order_groups = get_partial_order_groups(event_log)
        with open(temp_file, 'w') as outfile:
            json.dump(partial_order_groups, outfile, indent=4)

    return JsonResponse(partial_order_groups, safe=False)


def get_partial_order_groups(event_log):
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    df = df[[CASE_CONCEPT_NAME, DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY]]
    df[DEFAULT_TIMESTAMP_KEY] = df[DEFAULT_TIMESTAMP_KEY].astype(str)
    df = df.sort_values(by=[CASE_CONCEPT_NAME, DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY])
    partial_order_groups = {'totalNumberOfTraces': len(event_log), 'groups': {}}
    df.groupby(CASE_CONCEPT_NAME).apply(lambda x: check_for_partial_order(x, partial_order_groups))

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
