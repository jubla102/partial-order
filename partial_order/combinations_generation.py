import itertools

import pandas as pd
from django.conf import settings
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.statistics.traces.pandas import case_statistics
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY


def get_order_combinations(partial_order_trace):
    df = pd.DataFrame(partial_order_trace)

    unique_timestamps = df.drop_duplicates(subset=DEFAULT_TIMESTAMP_KEY, keep=False, inplace=False)
    unique_timestamps_events = unique_timestamps.to_dict('records')

    duplicated_timestamps_events = df[df.duplicated([DEFAULT_TIMESTAMP_KEY], keep=False)]

    # divides the trace into a list of events with the same timestamp
    partial_orders = []
    timestamps = duplicated_timestamps_events[DEFAULT_TIMESTAMP_KEY].unique()
    for timestamp in timestamps:
        partial_order = duplicated_timestamps_events.loc[
            duplicated_timestamps_events[DEFAULT_TIMESTAMP_KEY] == timestamp]
        partial_orders.append(partial_order.to_dict('records'))

    # generates all permutations of the partial orders
    permutations = []
    for partial_order in partial_orders:
        permutations.append(list(itertools.permutations(partial_order)))

    # cartesian product of the permutations
    cartesian_product = list(itertools.product(*permutations))

    case_information = get_case_information()
    combinations = []
    for p in cartesian_product:
        unsorted_trace = [element for tupl in p for element in tupl] + unique_timestamps_events
        combination = sorted(unsorted_trace, key=lambda x: x[DEFAULT_TIMESTAMP_KEY])
        activities = []
        key = ''
        for event in combination:
            activities.append(event[DEFAULT_NAME_KEY])
            key = ','.join(activities)

        combinations.append({'events': combination, 'frequency': get_frequency(key, case_information)})

    combinations.sort(key=lambda x: x['frequency'], reverse=True)
    return combinations


def get_case_information():
    df = log_converter.apply(settings.EVENT_LOG, variant=log_converter.Variants.TO_DATA_FRAME)
    variants_count = case_statistics.get_variant_statistics(df)
    return sorted(variants_count, key=lambda x: x[CASE_CONCEPT_NAME], reverse=True)


def get_frequency(key, case_information):
    for information in case_information:
        if key == information['variant']:
            return information[CASE_CONCEPT_NAME]

    return 0
