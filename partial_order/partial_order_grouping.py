from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util.constants import CASE_CONCEPT_NAME

from partial_order_detection import get_partial_orders_from_selected_file as get_partial_orders


def get_partial_order_groups():
    partial_order_log = get_partial_orders()
    df = log_converter.apply(partial_order_log, variant=log_converter.Variants.TO_DATA_FRAME)
    print(df)

    cases = df[CASE_CONCEPT_NAME].unique()
    print(cases)

    partial_order_groups = {}
    i = 0
    """
    for case_id in cases.size:
        partial_order_groups[i] = pd.DataFrame()
        case = df.loc[df[CASE_CONCEPT_NAME] == case_id]
        i += 1
        print(case)
    """

    if __name__ == '__main__':
        get_partial_order_groups()
