import os
import unittest

import pandas as pd
from parameterized import parameterized
from pm4py.objects.conversion.log import converter as log_converter

from partial_order import partial_order_detection


class TestPartialOrderDetection(unittest.TestCase):
    EVENT_LOG_ROOT = os.path.join(os.getcwd(), 'media/event_logs')

    @parameterized.expand([
        ("file contains 3 traces", "no-partial-orders.csv", 3),
        ("file contains 4 traces", "two-partial-order-groups.csv", 5)
    ])
    def test_total_number_of_traces(self, _, filename, groups):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, filename)
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_partial_order_groups(event_log)

        self.assertEqual(groups, partial_order_groups['totalNumberOfTraces'])

    @parameterized.expand([
        ("file contains 0 groups", "no-partial-orders.csv", 0),
        ("file contains 2 groups", "two-partial-order-groups.csv", 2)
    ])
    def test_number_of_groups(self, _, filename, groups):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, filename)
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_partial_order_groups(event_log)

        self.assertEqual(groups, len(partial_order_groups['groups']))

    def test_two_cases_in_group(self):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-order-groups.csv")
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_partial_order_groups(event_log)
        
        self.assertEqual(2, partial_order_groups['groups']['|a||bc||e||f|']['numberOfCases'])

    def test_one_cases_in_group(self):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-order-groups.csv")
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_partial_order_groups(event_log)

        self.assertEqual(1, partial_order_groups['groups']['|a||cd||g|']['numberOfCases'])


if __name__ == '__main__':
    unittest.main()
