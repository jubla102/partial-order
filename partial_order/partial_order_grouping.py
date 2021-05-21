import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util.constants import CASE_CONCEPT_NAME

from partial_order_detection import get_partial_orders_from_selected_file as get_partial_orders


def get_partial_order_groups():
    partial_order_log = get_partial_orders()
    df = log_converter.apply(partial_order_log, variant=log_converter.Variants.TO_DATA_FRAME)

    cases = df[CASE_CONCEPT_NAME].unique()
    """
    partial_order_groups_init is a 3 dimensional array that initially stores all partial orders in th following format:
    partial_order_groups_init[group_number][index_for_each_timestamp][index_for_events_with_the_same_timestamp]
    """
    partial_order_groups_init = [[0] * 10] * 10
    i = 0
    j = 0

    for case_id in cases:
        case = df.loc[df[CASE_CONCEPT_NAME] == case_id]
        # print(case)
        event_data = {'name': [str(case.iloc[0][0])], 'transition': [str(case.iloc[0][1])],
                      'timestamp': [pd.to_datetime(case.iloc[0][2])],
                      'case': [int(case.iloc[0][3])]}
        partial_order_groups_init[i][j] = pd.DataFrame(event_data)
        for event in range(1, len(case)):
            if case.iloc[event][2] == case.iloc[event - 1][2]:
                event_data = {'name': str(case.iloc[event][0]), 'transition': str(case.iloc[event][1]),
                              'timestamp': pd.to_datetime(case.iloc[event][2]),
                              'case': int(case.iloc[event][3])}
                partial_order_groups_init[i][j] = partial_order_groups_init[i][j].append(event_data,
                                                                                         ignore_index=True)
            else:
                j += 1
                event_data = {'name': [str(case.iloc[event][0])], 'transition': [str(case.iloc[event][1])],
                              'timestamp': [pd.to_datetime(case.iloc[event][2])],
                              'case': [int(case.iloc[event][3])]}
                partial_order_groups_init[i][j] = pd.DataFrame(event_data)

        print(partial_order_groups_init[i])
        i += 1
        j = 0


def test_dataframe():
    a = {'Car': ['a', 'b', 'c'], 'Type': ['big', 'smol', 'tiny']}
    df_a = pd.DataFrame(a)
    print(df_a)
    b = {'Car': 'd', 'Type': 'boogula'}
    df_a = df_a.append(b, ignore_index=True)
    print(df_a)


if __name__ == '__main__':
    test_dataframe()
    get_partial_order_groups()
