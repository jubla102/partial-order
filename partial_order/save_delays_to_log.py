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

    # also creates a copy to save the original log
    copyfile(event_log_path, event_log_path + '.org.xes')
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME, parameters=parameters)
    return df


"""
Returns the groups.json file content as a dictionary object
"""


def get_groups(groups_path):

    # create a copy of th original if it doesn't already exist
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


def save_delay_to_log(variant_path, groups_path, event_log_path):

    event_log_df = get_log(event_log_path)
    groups_dict = get_groups(groups_path)
    variant_dict = get_variant(variant_path)

    # save the delay from the user
    time_delay = variant_dict[DELAY]

    # store the sequence in which the events take place
    sequence = variant_dict[EVENTS]

    # group event_log_df by case Ids and then sort the groups by timestamp, followed by event names
    event_log_df = event_log_df.groupby([CASE_CONCEPT_NAME]).apply(
        lambda x: x.sort_values([DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY], ascending=True)).reset_index(drop=True)

    # sort the variant's group's caseIds in ascending order
    variant_dict[CASEIDS] = sorted(variant_dict[CASEIDS])

    # create a copy of the event_log_df
    log_copy = event_log_df

    # iterate over each caseId present in the selected group
    for caseId in variant_dict[CASEIDS]:

        # counter for delta modifier
        counter = 0

        # list to store all new timestamps
        new_time_list = list()

        # number ot cases in the selected variant's group
        length = len(log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId)])

        # iterate over the copy of the log to reorder the rows in event_log_df in the order that the user selected
        for idx, event in enumerate(log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId)]):
            event_log_df.loc[event_log_df[CASE_CONCEPT_NAME] == caseId].iloc[idx] = \
                log_copy.loc[
                    (log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == sequence[idx])].iloc[0]
            log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == event)] = \
                log_copy[(log_copy[CASE_CONCEPT_NAME] == caseId) & (log_copy[DEFAULT_NAME_KEY] == event)].iloc[1:]
            if idx == length - 1:
                break

        # store the timestamps in a list
        timestamps = event_log_df[log_copy[CASE_CONCEPT_NAME] == caseId][DEFAULT_TIMESTAMP_KEY].tolist()

        # append the first timestamp to the list of new timestamps
        new_time_list.append(timestamps[0])

        # the smallest variant will be 2 events
        # therefore, the smallest possible value for the first duplicate timestamp is 1
        partial_ind = 1

        # find the index of the first duplicate timestamp in the list of timestamps
        while not timestamps[partial_ind] == timestamps[partial_ind - 1]:
            new_time_list.append(timestamps[partial_ind])
            partial_ind += 1

        # iterate over each timestamp in the lsit of timestamps and then add the corresponding delay
        # starting from the first duplicate timestamp
        for ind, timestamp in enumerate(timestamps[partial_ind:]):
            if timestamp == timestamps[partial_ind + ind - 1]:

                # increment the delta modifier when the current timestamp is also a duplicate
                counter += 1

            # store delta value for the current timestamp
            delta = int(counter * time_delay)

            # add delta to the timestamp
            new_time = timestamp + timedelta(seconds=delta)

            # append the new timestamp to the list of new timestamps
            new_time_list.append(new_time)

        # get the index for the list of new timestamps from that of the dataframe for this caseId
        new_time_list_index = list(event_log_df[event_log_df[CASE_CONCEPT_NAME] == caseId]
                                   [DEFAULT_TIMESTAMP_KEY].index.values)

        # create a pandas Series object with the new timestamp list and its index list
        new_time_series = pd.Series(data=new_time_list, index=new_time_list_index)

        # overwrite the current timestamp column for caseId with the pandas Series object
        # this will add the new timestamps to the event_log_df
        event_log_df.loc[event_log_df[CASE_CONCEPT_NAME] == caseId, DEFAULT_TIMESTAMP_KEY] = new_time_series

    # delete the user selected variant's group information from the json file containing all groups' information
    if variant_dict[GROUP] in groups_dict[GROUPS]:
        del groups_dict[GROUPS][variant_dict[GROUP]]

    # write the new groups information into the same file, while the original groups file remains intact
    dump_to_json(groups_dict, groups_path)


if __name__ == '__main__':

    # add complete paths to the respective files here

    # complete path to the variant information from the user here
    variant_file_path = 'variant_file.json'

    # complete path to the json file containing all groups' information
    groups_file_path = 'groups_file.json'

    # complete path to the xes log file
    event_log_file_path = 'event_log_file.xes'

    # function that does everything (magic)
    save_delay_to_log(variant_file_path, groups_file_path, event_log_file_path)
