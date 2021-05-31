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
            "a": "#EE6352",
            "b": "#59CD90",
            "c": "#3FA7D6",
            "d": "#FAC05E",
            "e": "#F79D84",
            "f": "#53A548",
            "g": "#804E49",
            "h": "#A69CAC",
            "i": "#BAF2D8",
            "j": "#9F2042",
            "k": "#788585",
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
                                "activity": "c",
                                "timestamp": "2021-05-11 12:00"
                            },
                            {
                                "activity": "a",
                                "timestamp": "2021-05-11 12:00"
                            },
                            {
                                "activity": "d",
                                "timestamp": "2021-05-11 12:00"
                            }
                        ]
                    },
                    {
                        "caseId": 2,
                        "events": [
                            {
                                "activity": "c",
                                "timestamp": "2021-05-11 13:00"
                            },
                            {
                                "activity": "a",
                                "timestamp": "2021-05-11 13:00"
                            },
                            {
                                "activity": "d",
                                "timestamp": "2021-05-11 13:00"
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
                                "activity": "a",
                                "timestamp": "2021-05-11 12:01"
                            },
                            {
                                "activity": "b",
                                "timestamp": "2021-05-11 12:01"
                            },
                            {
                                "activity": "c",
                                "timestamp": "2021-05-11 12:01"
                            },
                            {
                                "activity": "d",
                                "timestamp": "2021-05-11 12:02"
                            },
                            {
                                "activity": "e",
                                "timestamp": "2021-05-11 12:02"
                            },
                            {
                                "activity": "f",
                                "timestamp": "2021-05-11 12:03"
                            },
                            {
                                "activity": "g",
                                "timestamp": "2021-05-11 12:03"
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
    absolute_file_path = os.path.join(event_logs_path, 'simple-test.xes')
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
