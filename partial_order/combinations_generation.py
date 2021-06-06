import itertools

import pandas as pd
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY


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

    combinations = []
    for p in cartesian_product:
        unsorted_trace = [element for tupl in p for element in tupl] + unique_timestamps_events
        combinations.append(sorted(unsorted_trace, key=lambda x: x[DEFAULT_TIMESTAMP_KEY]))

    return combinations


if __name__ == '__main__':
    case = [{'case:concept:name': 'B', 'concept:name': 'f', 'time:timestamp': '2021-05-02 12:06'},
            {'case:concept:name': 'B', 'concept:name': 'b', 'time:timestamp': '2021-05-02 12:01'},
            {'case:concept:name': 'B', 'concept:name': 'a', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'B', 'concept:name': 'e', 'time:timestamp': '2021-05-02 12:05'},
            {'case:concept:name': 'B', 'concept:name': 'c', 'time:timestamp': '2021-05-02 12:01'},
            {'case:concept:name': 'B', 'concept:name': 'g', 'time:timestamp': '2021-05-02 12:06'},
            {'case:concept:name': 'B', 'concept:name': 'd', 'time:timestamp': '2021-05-02 12:01'}]
    combinations = get_order_combinations(case)
    for combination in combinations:
        for event in combination:
            print(event['concept:name'], end=' ')
        print('')
