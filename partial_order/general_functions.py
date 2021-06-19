import json
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
    return {'colors': settings.COLORS,
            'longestActivityName': settings.LONGEST_ACTIVITY_NAME,
            'textWidths': settings.TEXT_WIDTHS}


def dupcheck(x):
    for elem in x:
        if x.count(elem) > 1:
            return True
    return False


def generate_colors(activities_length):
    if (activities_length > 10):
        color_palette = sns.color_palette(None, 10).as_hex()
        activities_length -= 10
    else:
        color_palette = sns.color_palette(None, activities_length).as_hex()
        return color_palette
    if (activities_length > 10):
        color_palette = color_palette + sns.color_palette("pastel", 10).as_hex()
        activities_length -= 10
    else:
        color_palette = color_palette + sns.color_palette("pastel", activities_length).as_hex()
        return color_palette
    if (activities_length >= 1):
        color_palette = color_palette + sns.color_palette("bright", activities_length).as_hex()
        return color_palette


def get_colors(activities):
    color_palette = generate_colors(len(activities))
    colors = {}
    for i, activity in enumerate(activities):
        colors[activity] = color_palette[i]

    return colors


def get_form_data(request, key):
    return json.loads(request.POST.dict()[key])


if __name__ == '__main__':
    colors = get_colors((31))
    print("final: ", len(colors), colors)
