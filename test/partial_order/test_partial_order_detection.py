import os
import unittest

import pandas as pd
from parameterized import parameterized
from pm4py.objects.conversion.log import converter as log_converter

from partial_order import partial_order_detection


class TestPartialOrderDetection(unittest.TestCase):
    EVENT_LOG_ROOT = os.path.join(os.getcwd(), 'media/event_logs')

    @parameterized.expand([
        ("no partial orders should return size 0", "no-partial-orders.csv", 0),
        ("two partial orders should return size 2", "two-partial-orders.csv", 2)
    ])
    def test_number_of_detected_partial_orders(self, _, filename, expected_size):
        event_log_absolute_path = os.path.join(TestPartialOrderDetection.EVENT_LOG_ROOT, filename)
        df = pd.read_csv(event_log_absolute_path, sep=";")
        event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
        number_of_partial_orders = len(partial_order_detection.get_partial_orders_from_event_log(event_log))

        self.assertEqual(expected_size, number_of_partial_orders)


if __name__ == '__main__':
    unittest.main()
