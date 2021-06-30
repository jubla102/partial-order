from django.test import TestCase

from partial_order import general_functions


class TestGetLongestActivityName(TestCase):
    """
    Testing if the length of the longest activity name is equal to the expected value
    """

    def test_get_longest_activity_name_7(self):
        """
        Mock activities list with longest activity name containing 7 characters
        """
        mock_activities = ['A', 'BB', 'C', 'DDD', 'EEEEEEE', 'FFFF']

        combinations = general_functions.get_longest_activity_name(mock_activities)

        self.assertEqual(len(combinations), 7)

    def test_get_longest_activity_name_10(self):
        """
        Mock activities list with longest activity name containing 10 characters
        """
        mock_activities = ['kasnda', 'ASKD', 'HO Ssd', 'GFS', 'AS SAAA DA', 'A']

        combinations = general_functions.get_longest_activity_name(mock_activities)

        self.assertEqual(len(combinations), 10)

    def test_get_longest_activity_name_3(self):
        """
        Mock activities list with longest activity name containing 3 characters
        """
        mock_activities = ['123', '46', '9', '374', '1', '90']

        combinations = general_functions.get_longest_activity_name(mock_activities)

        self.assertEqual(len(combinations), 3)
