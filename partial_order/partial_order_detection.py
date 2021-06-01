import os

import pandas as pd
from django.http import JsonResponse
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
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


def get_partial_orders_from_selected_file():
    """
    simple-test.xes event log contains 9 cases.
    The following case ids are partial orders: 1, 4, 6, 7, 8, 9
    The groups are: (1, 7, 8), (4, 6), (9)

    TODO Replace hard coded file by user selection
    """
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    absolute_file_path = os.path.join(event_logs_path, 'Sepsis_Cases-Event_Log.xes')
    event_log = importer.apply(absolute_file_path)

    return get_partial_orders_from_event_log(event_log)


def get_partial_orders_from_event_log(event_log):
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    case_identifiers = df[CASE_CONCEPT_NAME].unique()
    partial_orders = pd.DataFrame()
    for case_id in case_identifiers:
        case = df.loc[df[CASE_CONCEPT_NAME] == case_id]
        if is_partial_order(case):
            partial_orders = partial_orders.append(case)

    return log_converter.apply(partial_orders, variant=log_converter.Variants.TO_EVENT_LOG)


def is_partial_order(case):
    return not case[DEFAULT_TIMESTAMP_KEY].is_unique


if __name__ == '__main__':
    print(get_partial_orders_from_selected_file())
