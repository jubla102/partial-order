from datetime import datetime, timedelta
import json

from pm4py.objects.log.importer.xes import importer
from pm4py.objects.conversion.log import converter as log_converter


def get_test_groups():
    with open('test_groups.json') as test_groups_file:
        data = json.load(test_groups_file)
    return data

def dump_to_json(data, file_name):
    with open(file_name + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def time_to_datetime(time_string):
    time_datetime = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S%z')
    return time_datetime

def time_in_seconds(time_string):
    time_datetime = time_to_datetime(time_string)
    delta_seconds = time_datetime.second + time_datetime.minute*60 + time_datetime.hour*3600
    return delta_seconds

"""
TEST - get the time in minutes
"""
def time_in_minutes(time_string):
    time_datetime = time_to_datetime(time_string)
    delta_minutes = time_datetime.second/60.0 + time_datetime.minute + time_datetime.hour*60
    return delta_minutes

"""
TEST - get the time in hours
"""
def time_in_hours(time_string):
    time_datetime = time_to_datetime(time_string)
    delta_hours = time_datetime.second/3600.0 + time_datetime.minute/60.0 + time_datetime.hour
    return delta_hours

def modify_log():
    test_log = open('test_log.xes')
    event_log = importer.apply(test_log)
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)


if __name__ == '__main__':
    time = '2014-10-22 21:15:41+02:00'
    print(time_to_datetime(time))
    # print(time_to_datetime(time) + timedelta(hours=time_in_hours(time)))
    # print(time_to_datetime(time) + timedelta(minutes=time_in_minutes(time)))
    print(time_to_datetime(time) + timedelta(seconds=time_in_seconds(time)))
    groups = get_test_groups()
    print(groups.keys())
    dump_to_json(groups, 'test_groups')
