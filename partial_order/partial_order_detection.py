import os

import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from bootstrapdjango import settings


def get_partial_orders_from_event_log():
    """
    simple-test.xes event log contains 9 cases.
    The following case ids are partial orders: 1, 4, 6, 7, 8, 9
    The groups are: (1, 7, 8), (4, 6), (9)
    """
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    event_log = os.path.join(event_logs_path, 'simple-test.xes')
    log = importer.apply(event_log)
    df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    case_identifiers = df[CASE_CONCEPT_NAME].unique()

    partial_orders = pd.DataFrame()
    for case_id in case_identifiers:
        case = df.loc[df[CASE_CONCEPT_NAME] == case_id]
        if is_partial_order(case):
            partial_orders = partial_orders.append(case)

    return log_converter.apply(partial_orders, variant=log_converter.Variants.TO_EVENT_LOG)


def is_partial_order(case):
    return not case[DEFAULT_TIMESTAMP_KEY].is_unique


if __name__ == "__main__":
    print(get_partial_orders_from_event_log())
