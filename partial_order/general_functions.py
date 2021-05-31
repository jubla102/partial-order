import os

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer

from bootstrapdjango import settings


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


if __name__ == '__main__':
    print(max_trace_length())
