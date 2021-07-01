from django.test import TestCase

from partial_order import general_functions


class TestGenerateColors(TestCase):
    """
    Testing if the number of colors generated is equal to the number of activities
    """

    def test_generate_colors_5(self):
        color_palette = general_functions.generate_colors(5)

        self.assertEqual(5, len(color_palette))

    def test_generate_colors_10(self):
        color_palette = general_functions.generate_colors(10)

        self.assertEqual(10, len(color_palette))

    def test_generate_colors_15(self):
        color_palette = general_functions.generate_colors(15)

        self.assertEqual(15, len(color_palette))

    def test_generate_colors_25(self):
        color_palette = general_functions.generate_colors(25)

        self.assertEqual(25, len(color_palette))

    def test_generate_colors_35(self):
        color_palette = general_functions.generate_colors(35)

        self.assertEqual(35, len(color_palette))

    """
    Testing if the number of unique colors generated is equal to the number of activities
    """

    def test_generate_unique_colors_5(self):
        color_palette = general_functions.generate_colors(5)

        self.assertEqual(5, len(set(color_palette)))

    def test_generate_unique_colors_10(self):
        color_palette = general_functions.generate_colors(10)

        self.assertEqual(10, len(set(color_palette)))

    def test_generate_unique_colors_15(self):
        color_palette = general_functions.generate_colors(15)

        self.assertEqual(15, len(set(color_palette)))

    def test_generate_unique_colors_25(self):
        color_palette = general_functions.generate_colors(25)

        self.assertEqual(25, len(set(color_palette)))

    def test_generate_unique_colors_35(self):
        """
        Currently the application can generate at most 30 colors
        """
        color_palette = general_functions.generate_colors(35)

        self.assertEqual(30, len(set(color_palette)))
