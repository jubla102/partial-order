import math
import unittest

from parameterized import parameterized

from partial_order import combinations_generation


class TestCombinationsGeneration(unittest.TestCase):

    @parameterized.expand([
        ("[1, 2] should return 2 permutations", [1, 2], [[1, 2], [2, 1]]),
        ("[1, 2, 3] should return 2 permutations", [1, 2, 3], [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1],
        ])
    ])
    def test_compare_permutations(self, _, activities, expected_permutations):
        permutations = combinations_generation.heaps_permutations(activities)

        self.assertEqual(expected_permutations, permutations)

    @parameterized.expand([
        ("[1, 2, 3, 4] should return 4! = 24 permutations", [1, 2, 3, 4]),
        ("[[1, 2, 3, 4, 5] should return 5! = 120 permutations", [1, 2, 3, 4, 5])
    ])
    def test_compare_number_of_permutations(self, _, activities):
        permutations = combinations_generation.heaps_permutations(activities)

        self.assertEqual(len(permutations), math.factorial(len(activities)))
