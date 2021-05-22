import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util.constants import CASE_CONCEPT_NAME

from partial_order_detection import get_partial_orders_from_selected_file as get_partial_orders

CONCEPT_INDEX = 'concept:index'
CONCEPT_NAME = 'concept:name'
LIFECYCLE_TRANSITION = 'lifecycle:transition'


def get_partial_order_dataframes():
    partial_order_log = get_partial_orders()
    df = log_converter.apply(partial_order_log, variant=log_converter.Variants.TO_DATA_FRAME)
    cases = df[CASE_CONCEPT_NAME].unique()

    partial_order_dataframes = list()

    i = -1

    for case_id in cases:
        i += 1

        case = df.loc[df[CASE_CONCEPT_NAME] == case_id]

        ind_list = case.index.tolist()
        ind = 0

        ind_list[0] = ind

        partial_order_dataframes.append([])

        partial_order_dataframes[i] = pd.DataFrame()
        partial_order_dataframes[i] = partial_order_dataframes[i].append(case.iloc[0], ignore_index=True)

        for event in range(1, len(case)):
            if case.iloc[event - 1][2] == case.iloc[event][2]:
                partial_order_dataframes[i] = partial_order_dataframes[i].append(case.iloc[event], ignore_index=True)
            else:
                ind += 1
                partial_order_dataframes[i] = partial_order_dataframes[i].append(case.iloc[event],
                                                                                 ignore_index=True)
            ind_list[event] = ind

        partial_order_dataframes[i].index = ind_list
        partial_order_dataframes[i].reset_index(inplace=True)
        partial_order_dataframes[i] = partial_order_dataframes[i].rename(columns={'index': CONCEPT_INDEX})
        partial_order_dataframes[i].astype({CONCEPT_INDEX: 'int64'}).dtypes

        for i in range(0, len(partial_order_dataframes)):
            partial_order_dataframes[i] = partial_order_dataframes[i].sort_values([CONCEPT_INDEX], ascending=True) \
                .groupby([CONCEPT_INDEX], sort=False) \
                .apply(lambda x: x.sort_values([CONCEPT_NAME], ascending=True)) \
                .reset_index(drop=True)

    return partial_order_dataframes


def get_partial_order_groups():
    partial_order_dataframes = get_partial_order_dataframes()

    order_attributes = [CONCEPT_INDEX, CONCEPT_NAME, LIFECYCLE_TRANSITION, CASE_CONCEPT_NAME]
    group_attributes = [CONCEPT_INDEX, CONCEPT_NAME, LIFECYCLE_TRANSITION]

    partial_orders = list()

    for i in range(0, len(partial_order_dataframes)):
        partial_orders.append([])
        partial_orders[i] = partial_order_dataframes[i][order_attributes]

    partial_order_groups = list()

    g = 0

    while len(partial_orders):

        partial_order_groups.append([])
        partial_order_groups[g].append([])
        partial_order_groups[g][0] = pd.DataFrame()
        partial_order_groups[g][0] = partial_orders[0][group_attributes]
        partial_order_groups[g][0] = partial_order_groups[g][0].sort_values([CONCEPT_INDEX], ascending=True) \
            .groupby([CONCEPT_INDEX], sort=False) \
            .apply(lambda x: x.sort_values([CONCEPT_INDEX], ascending=True)) \
            .reset_index(drop=True)

        partial_order_groups[g].append([])
        partial_order_groups[g][1] = pd.DataFrame(columns=[CASE_CONCEPT_NAME])
        val = pd.Series([partial_orders[0][CASE_CONCEPT_NAME][0]], dtype='str')
        partial_order_groups[g][1][CASE_CONCEPT_NAME] = \
            partial_order_groups[g][1][CASE_CONCEPT_NAME].append(val, ignore_index=True)

        partial_orders.remove(partial_orders[0])

        for case in range(0, len(partial_orders)):
            if partial_order_groups[g][0].equals(partial_orders[case][group_attributes]):
                if partial_orders[case][CASE_CONCEPT_NAME][0] not in \
                        partial_order_groups[g][0][CASE_CONCEPT_NAME]:
                    partial_order_groups[g][1][CASE_CONCEPT_NAME].append(
                        [partial_orders[case][CASE_CONCEPT_NAME][0]], ignore_index=True)
                partial_orders.remove(partial_orders[case])
                case -= 1
        g += 1

    return partial_order_groups


if __name__ == '__main__':
    partial_order_groups_main = get_partial_order_groups()
    partial_orders_main = get_partial_order_dataframes()
    for i in range(0, len(partial_order_groups_main)):
        print('Group ', i + 1)
        """
        partial_order_groups_main[i][j]
        i = group index
        j = 0: dataframe with group information
        j = 1: dataframe with case ID's corresponding to the group
        """
        print(partial_order_groups_main[i][0])
        print('Corresponding cases')
        print(partial_order_groups_main[i][1])
