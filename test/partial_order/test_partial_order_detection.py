import os

from django.test import TestCase
from parameterized import parameterized
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

from partial_order import partial_order_detection


class TestPartialOrderDetection(TestCase):
    EVENT_LOG_ROOT = os.path.join(os.getcwd(), 'test/partial_order/media/event_logs')

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
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-orders.xes")
        log = xes_importer.apply(event_log_absolute_path)
        df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(df)

        self.assertEqual(2, partial_order_groups['|a||bc|']['numberOfCases'])

    def test_one_cases_in_group(self):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, "two-partial-orders.xes")
        log = xes_importer.apply(event_log_absolute_path)
        df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        partial_order_groups = partial_order_detection.get_sorted_partial_order_groups(df)

        self.assertEqual(1, partial_order_groups['|e||fg|']['numberOfCases'])
