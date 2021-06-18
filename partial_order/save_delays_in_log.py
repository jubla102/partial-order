from datetime import datetime, timedelta
import json
import os.path
from shutil import copyfile

import pandas as pd
from pm4py.objects.log.importer.xes import importer

from pm4py.objects.conversion.log import converter as log_converter

from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY

# CONSTANTS
GROUP = 'group'
GROUPS = 'groups'
EVENTS = 'events'
CASEIDS = 'caseIds'
DELAY = 'delay'

"""
Write the dictionary object to a json file
"""


def dump_to_json(data, groups_path):
    if not os.path.isfile(groups_path + '.org.json'):
        copyfile(groups_path, groups_path + '.org.json')
    with open(groups_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


"""
Returns the event log as a dataframe object, sorted by timestamps
"""


def get_log(event_log_path):
    parameters = {"timestamp_sort": True}
    event_log = importer.apply(event_log_path)
    copyfile(event_log_path, event_log_path + '.org.xes')
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME, parameters=parameters)
    return df


"""
Returns the groups.json file content as a dictionary object
"""


def get_groups(groups_path):
    if not os.path.isfile(groups_path + '.org.json'):
        copyfile(groups_path, groups_path + '.org.json')
    with open(groups_path + '.org.json') as test_groups_file:
        data = json.load(test_groups_file)
    return data


"""
Returns the group information and delay from the frontend as a dictionary object
"""


def get_variant(variant_path):
    with open(variant_path) as test_group_info:
        data = json.load(test_group_info)
    return data


"""
Deletes the group information from the groups file and then writes the new timestamps into the log file
"""


def save_delay_in_log(variant_path, groups_path, event_log_path):
    event_log_df = get_log(event_log_path)
    groups_dict = get_groups(groups_path)
    variant_dict = get_variant(variant_path)

    time_delay = variant_dict[DELAY]
    sequence = variant_dict[EVENTS]

    event_log_df = event_log_df.groupby([CASE_CONCEPT_NAME]).apply(
        lambda x: x.sort_values([DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY], ascending=True)).reset_index(drop=True)

    variant_dict[CASEIDS] = sorted(variant_dict[CASEIDS])

    log_copy = event_log_df

    for caseId in variant_dict[CASEIDS]:
        counter = 0

        new_time_list = list()

        length = len(log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId)])

        for idx, event in enumerate(log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId)]):
            event_log_df.loc[event_log_df[CASE_CONCEPT_NAME] == caseId].iloc[idx] = \
                log_copy.loc[
                    (log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == sequence[idx])].iloc[0]
            log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == event)] = \
                log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == event)].iloc[1:]
            if idx == length - 1:
                break

        timestamps = event_log_df[log_copy[CASE_CONCEPT_NAME] == caseId][DEFAULT_TIMESTAMP_KEY].tolist()

        new_time_list.append(timestamps[0])

        partial_ind = 1
        while not timestamps[partial_ind] == timestamps[partial_ind - 1]:
            new_time_list.append(timestamps[partial_ind])
            partial_ind += 1

        for ind, timestamp in enumerate(timestamps[partial_ind:]):
            if timestamp == timestamps[partial_ind + ind - 1]:
                counter += 1

            delta = int(counter * time_delay)
            new_time = timestamp + timedelta(seconds=delta)
            new_time_list.append(new_time)

        new_time_list_index = list(event_log_df[event_log_df[CASE_CONCEPT_NAME] == caseId]
                                   [DEFAULT_TIMESTAMP_KEY].index.values)

        new_time_series = pd.Series(data=new_time_list, index=new_time_list_index)

        event_log_df.replace(to_replace=
                             event_log_df[event_log_df[CASE_CONCEPT_NAME] == caseId][DEFAULT_TIMESTAMP_KEY].values,
                             value=new_time_series, inplace=True)

    if variant_dict[GROUP] in groups_dict[GROUPS]:
        del groups_dict[GROUPS][variant_dict[GROUP]]

    dump_to_json(groups_dict, groups_path)


if __name__ == '__main__':
    variant_file_path = 'variant_file.json'
    groups_file_path = 'groups_file.json'
    event_log_file_path = 'event_log_file.xes'
    save_delay_in_log(variant_file_path, groups_file_path, event_log_file_path)
