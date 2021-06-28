from unittest.mock import patch

from django.test import TestCase, override_settings

from partial_order import combinations_generation


# EVENT_LOG and get_case_information are patched because they are not needed here
@override_settings(EVENT_LOG={})
@patch('partial_order.combinations_generation.get_case_information')
class TestCombinationsGeneration(TestCase):

    def test_trace_contains_one_partial_order(self, mock_get_case_information):
        """
        The events a - d are partial orders and therefore there are 4! = 24 possible orders.
        """
        trace = [
            {'case:concept:name': 'A', 'concept:name': 'a', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'A', 'concept:name': 'b', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'A', 'concept:name': 'c', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'A', 'concept:name': 'd', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'A', 'concept:name': 'e', 'time:timestamp': '2021-05-02 13:00'},
            {'case:concept:name': 'A', 'concept:name': 'f', 'time:timestamp': '2021-05-02 14:00'},
        ]
        mock_get_case_information.return_value = []

        combinations = combinations_generation.get_order_combinations(trace)

        self.assertEqual(len(combinations), 24)

    def test_trace_contains_two_partial_orders(self, mock_get_case_information):
        """
        There are 6 possible orders for partial ordered events b, c, d
        and 2 possible orders for partial ordered events f, g.
        Each of these orders can be combined. Therefore,
        in total there are 12 possible orders.
        """
        trace = [
            {'case:concept:name': 'B', 'concept:name': 'f', 'time:timestamp': '2021-05-02 12:06'},
            {'case:concept:name': 'B', 'concept:name': 'b', 'time:timestamp': '2021-05-02 12:01'},
            {'case:concept:name': 'B', 'concept:name': 'a', 'time:timestamp': '2021-05-02 12:00'},
            {'case:concept:name': 'B', 'concept:name': 'e', 'time:timestamp': '2021-05-02 12:05'},
            {'case:concept:name': 'B', 'concept:name': 'c', 'time:timestamp': '2021-05-02 12:01'},
            {'case:concept:name': 'B', 'concept:name': 'g', 'time:timestamp': '2021-05-02 12:06'},
            {'case:concept:name': 'B', 'concept:name': 'd', 'time:timestamp': '2021-05-02 12:01'}
        ]
        mock_get_case_information.return_value = []

        combinations = combinations_generation.get_order_combinations(trace)

        self.assertEqual(len(combinations), 12)
