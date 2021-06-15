import os

import seaborn as sns
from django.conf import settings


def get_selected_file_path():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    return os.path.join(event_logs_path, settings.EVENT_LOG_NAME)


def get_groups_file_path():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "temp")
    file_name = 'groups_' + os.path.splitext(settings.EVENT_LOG_NAME)[0] + '.json'
    return os.path.join(event_logs_path, file_name)


def get_longest_activity_name(activities):
    longest_activity_name = ''
    for activity in activities:
        if len(longest_activity_name) < len(activity):
            longest_activity_name = activity

    return longest_activity_name


def get_meta_data():
    return {'colors': settings.COLORS, 'longestActivityName': settings.LONGEST_ACTIVITY_NAME}


def get_colors(activities):
    color_palette = sns.color_palette(None, len(activities)).as_hex()
    colors = {}
    for i, activity in enumerate(activities):
        colors[activity] = color_palette[i]

    return colors
