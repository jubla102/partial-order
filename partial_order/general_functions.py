import os

from django.conf import settings
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer


def max_trace_length():
    """
        Returns
        -------
        result: maximum length of a trace in an event log
    """
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    absolute_file_path = os.path.join(event_logs_path, 'simple-test.xes')
    event_log = importer.apply(absolute_file_path)
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    val = df.groupby(["case:concept:name"]).count().max()
    return val["concept:name"]


def get_selected_file_path():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    return os.path.join(event_logs_path, settings.EVENT_LOG_NAME)


def get_groups_file_path():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "temp")
    file_name = 'groups_' + os.path.splitext(settings.EVENT_LOG_NAME)[0] + '.json'
    return os.path.join(event_logs_path, file_name)


def get_colors_file_path():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "temp")
    file_name = 'colors_' + os.path.splitext(settings.EVENT_LOG_NAME)[0] + '.json'
    return os.path.join(event_logs_path, file_name)


def get_number_of_traces():
    file = get_selected_file_path()
    event_log = importer.apply(file)
    return len(event_log)


if __name__ == '__main__':
    print(max_trace_length())
