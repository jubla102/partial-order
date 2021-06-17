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
Returns the event log as a dataframe object, sorted by timestamps
"""


def get_log():
    parameters = {"timestamp_sort": True}
    event_log = importer.apply('test_log.xes')
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME, parameters=parameters)
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
    event_log_df = get_log()
    groups_dict = get_groups()
    group_dict = get_selected_group()

    time_delay = group_dict['delay']
    for caseId in group_dict['caseIds']:
        counter = 0

        timestamps = event_log_df[event_log_df['case:concept:name'] == caseId]['time:timestamp'].tolist()

        temp = set()
        for idx, val in enumerate(timestamps):
            check = val in temp
            print(check)
            if check:
                partial_ind = idx
                break
            else:
                temp.add(val)

        print(partial_ind)

        for ind, timestamp in \
                enumerate(timestamps[partial_ind:]):
            if timestamp == timestamps[ind - 1]:
                counter += 1
            delta = int(counter * time_delay)
            event_log_df[event_log_df['case:concept:name'] == caseId].at[ind, 'time:timestamp']= \
                timestamp + timedelta(seconds=delta)

    if group_dict['group'] in groups_dict['groups']:
        del groups_dict['groups'][group_dict['group']]

    dump_to_json(groups_dict, 'modified_test_groups')

    print(event_log_df[event_log_df['case:concept:name'] == 'A']['time:timestamp'].iloc[2])


if __name__ == '__main__':
    save_delay_in_log()
