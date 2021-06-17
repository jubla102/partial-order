from datetime import datetime, timedelta
import json

from pm4py.objects.log.importer.xes import importer

from pm4py.objects.conversion.log import converter as log_converter


"""
Write the dictionary object to a json file
"""


def dump_to_json(data, file_name):
    with open(file_name + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


"""
Convert the time from a string object to a datetime object
"""


def time_to_datetime(time_string):
    time_datetime = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S%z')
    return time_datetime

"""
Add delta to a timestamp and return the new timestamp as a datetime object
"""


def add_time(time_datetime, delta_seconds):
    if not isinstance(time_datetime, datetime):
        time_datetime = time_to_datetime(time_datetime)

    return time_datetime + timedelta(seconds=delta_seconds)


"""
Returns the event log as a dataframe object
"""


def get_log():
    event_log = importer.apply('test_log.xes')
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)
    return df


"""
Returns the groups.json file content as a dictionary object
"""


def get_groups():
    with open('test_groups.json') as test_groups_file:
        data = json.load(test_groups_file)
    return data


"""
Returns the group information and delay from the frontend as a dictionary object
"""


def get_selected_group():
    with open('test_group_info.json') as test_group_info:
        data = json.load(test_group_info)
    return data


"""
Deletes the group information from the groups file and then writes the new timestamps into the log file
"""


def save_delay_in_log():
    time = '2014-10-22 21:15:41+02:00'
    event_log_df = get_log()
    groups_dict = get_groups()
    group_dict = get_selected_group()
    print(time)
    print(event_log_df)
    print(groups_dict['groups']['|ER Registration||ER Triage||ER Sepsis Triage||CRPLacticAcidLeucocytes||IV '
                                'Liquid||IV Antibiotics|']['caseIds'])
    print(group_dict['delay'])


if __name__ == '__main__':
    save_delay_in_log()
