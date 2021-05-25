import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY

from partial_order_detection import get_partial_orders_from_selected_file as get_partial_orders

CONCEPT_INDEX = 'concept:index'
INDEX = 'index'
INT = 'int64'
STRING = 'str'


def get_partial_order_sequences():
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
        partial_order_dataframes[i] = partial_order_dataframes[i].rename(columns={INDEX: CONCEPT_INDEX})
        partial_order_dataframes[i].astype({CONCEPT_INDEX: INT}).dtypes

    for j in range(0, len(partial_order_dataframes)):
        partial_order_dataframes[j] = partial_order_dataframes[j].sort_values([CONCEPT_INDEX], ascending=True) \
            .groupby([CONCEPT_INDEX], sort=False) \
            .apply(lambda x: x.sort_values([DEFAULT_NAME_KEY], ascending=True)) \
            .reset_index(drop=True)

    return partial_order_dataframes


def get_partial_order_group_sequences():
    partial_order_dataframes = get_partial_order_sequences()

    order_attributes = [CONCEPT_INDEX, DEFAULT_NAME_KEY, CASE_CONCEPT_NAME]
    group_attributes = [CONCEPT_INDEX, DEFAULT_NAME_KEY]

    partial_orders = list()

    for k in range(0, len(partial_order_dataframes)):
        partial_orders.append([])
        partial_orders[k] = pd.DataFrame()
        partial_orders[k] = partial_order_dataframes[k][order_attributes]

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
        partial_order_groups[g][1] = pd.DataFrame()
        case_id = pd.Series(partial_orders[0][CASE_CONCEPT_NAME][0], index=[CASE_CONCEPT_NAME])
        partial_order_groups[g][1] = partial_order_groups[g][1].append(case_id, ignore_index=True)

        partial_orders.remove(partial_orders[0])

        case = 0

        while case < len(partial_orders):
            if partial_order_groups[g][0].equals(partial_orders[case][group_attributes]):
                exists = partial_orders[case][CASE_CONCEPT_NAME][0] in partial_order_groups[g][1][CASE_CONCEPT_NAME]
                if not exists:
                    case_val = pd.Series(partial_orders[case][CASE_CONCEPT_NAME][0], index=[CASE_CONCEPT_NAME])
                    partial_order_groups[g][1] = partial_order_groups[g][1].append(case_val, ignore_index=True)

                del partial_orders[case]
            case += 1
        g += 1

    return partial_order_groups


def write_to_text_file():
    case_attributes = [CONCEPT_INDEX, DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY]

    partial_order_groups_file = get_partial_order_group_sequences()
    partial_orders_file = get_partial_order_sequences()
    file = open("partial_order_grouping_output.txt", "w")
    file.write('All partial orders with sequencing information and timestamps')
    file.writelines('\n')
    file.writelines('\n')
    for order in range(0, len(partial_orders_file)):
        case_num = 'Case ' + str(partial_orders_file[order][CASE_CONCEPT_NAME].iloc[0])
        file.write(case_num)
        file.writelines('\n')
        file.write(partial_orders_file[order][case_attributes].to_string(index=False))
        file.writelines('\n')
        file.writelines('\n')

    file.writelines('\n')
    file.write('Partial order groups with sequencing information and corresponding case ID\'s')
    file.writelines('\n')
    file.writelines('\n')

    for group in range(0, len(partial_order_groups_file)):
        group_num = 'Group ' + str(group + 1)
        file.write(group_num)
        file.writelines('\n')
        file.write(partial_order_groups_file[group][0].to_string(index=False))
        file.writelines('\n')
        file.writelines('\n')
        cases = group_num + ' cases'
        file.write(cases)
        file.writelines('\n')
        file.write(partial_order_groups_file[group][1][CASE_CONCEPT_NAME].to_string(index=False))
        file.writelines('\n')
        file.writelines('\n')

    file.close()


if __name__ == '__main__':
    write_to_text_file()
    partial_order_groups_main = get_partial_order_group_sequences()
    partial_orders_main = get_partial_order_sequences()
    temp = partial_order_groups_main[0][1][CASE_CONCEPT_NAME][0]
    for case in range(0, len(partial_orders_main)):
        if partial_orders_main[case][CASE_CONCEPT_NAME][0] == temp:
            print(partial_orders_main[case])

    """
    group[i]
    i = Group index
    
    Call group[i]['cases']
    'cases' = List of cases (with all information)
    *** cases must not be in data frame. use dictionary ***
    """
    # print('All partial orders with sequencing information and timestamps')
    # print(partial_orders_main)
    # print('Partial order groups with sequencing information and corresponding case ID\'s')
    # for g in range(0, len(partial_order_groups_main)):
    # print('Group ', g + 1)
    """
    partial_order_groups_main[i][j]
    i = group index
    j = 0: dataframe with group information
    j = 1: dataframe with case ID's corresponding to the group
    """
    """
    partial_orders_main[i]
    i = dataframe with partial order information
    """

    """
    [
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
]
    """
    # print(partial_order_groups_main[g][0])
    # print('Corresponding cases')
    # print(partial_order_groups_main[g][1])
