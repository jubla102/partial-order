import json

import seaborn as sns

from partial_order.general_functions import get_colors_file_path


def get_colors(activities):
    color_palette = sns.color_palette(None, len(activities)).as_hex()
    colors = {}
    for i, activity in enumerate(activities):
        colors[activity] = color_palette[i]

    return colors


def get_colors_from_file():
    color_file = get_colors_file_path()
    with open(color_file) as color_file:
        return json.load(color_file)
