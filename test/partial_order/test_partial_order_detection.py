import os
import unittest

import pandas as pd
from django.test import TestCase
from parameterized import parameterized
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

from partial_order import partial_order_detection


class TestPartialOrderDetection(TestCase):
    EVENT_LOG_ROOT = os.path.join(os.getcwd(), 'test/partial_order/media/event_logs')

    @parameterized.expand([
        ("file contains 3 traces", "no-partial-orders.csv", 3),
        ("file contains 4 traces", "two-partial-order-groups.csv", 5)
    ])
    def test_total_number_of_traces(self, _, filename, groups):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, filename)
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(event_log)

        self.assertEqual(groups, partial_order_groups['totalNumberOfTraces'])

    @parameterized.expand([
        ("file contains 0 groups", "no-partial-orders.xes", 0),
        ("file contains 2 groups", "two-partial-orders.xes", 2)
    ])
    def test_number_of_groups(self, _, filename, groups):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, filename)
        log = xes_importer.apply(event_log_absolute_path)
        df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(df)

        self.assertEqual(groups, len(partial_order_groups))

    def test_two_cases_in_group(self):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-order-groups.csv")
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(event_log)

        self.assertEqual(2, partial_order_groups['groups']['|a||bc||e||f|']['numberOfCases'])

    def test_one_cases_in_group(self):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-order-groups.csv")
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(event_log)

        self.assertEqual(1, partial_order_groups['groups']['|a||cd||g|']['numberOfCases'])


if __name__ == '__main__':
    unittest.main()
