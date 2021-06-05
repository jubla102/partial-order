import json
import os

import seaborn as sns

from bootstrapdjango import settings


def get_colors(activities):
    color_palette = sns.color_palette(None, len(activities)).as_hex()
    colors = {}
    for i, activity in enumerate(activities):
        colors[activity] = color_palette[i]

    return colors


def get_colors_from_file():
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp")
    temp_color_file = os.path.join(temp_path, 'colors_Sepsis_Cases-Event_Log.json')
    with open(temp_color_file) as color_file:
        return json.load(color_file)
