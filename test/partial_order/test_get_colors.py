from django.test import TestCase

from partial_order import general_functions


class TestGetColors(TestCase):
    """
    Testing if every activity in the activities list has a color
    """

    def test_get_colors_6(self):
        """
        Mock activities list with 6 activities
        """
        mock_activities = ['A', 'BB', 'C', 'DDD', 'EEEEEEE', 'FFFF']

        colors = general_functions.get_colors(mock_activities)

        self.assertEqual(len(mock_activities), len(colors))

    def test_get_colors_10(self):
        """
        Mock activities list with 10 activities
        """
        mock_activities = ['A', 'BB', 'C', 'DDD', 'EEEEEEE', 'FFFF', 'SSDA', 'AA', 'DW', 'EFG']

        colors = general_functions.get_colors(mock_activities)

        self.assertEqual(len(mock_activities), len(colors))

    def test_get_colors_12(self):
        """
        Mock activities list with 6 activities
        """
        mock_activities = ['A', 'BB', 'C', 'DDD', 'EEEEEEE', 'FFFF', 'SSDA', 'AA', 'DW', 'EFG', '123', 'k s']

        colors = general_functions.get_colors(mock_activities)

        self.assertEqual(len(mock_activities), len(colors))
