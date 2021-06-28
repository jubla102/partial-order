import os.path
from datetime import timedelta
from shutil import copyfile

import numpy as np
import pandas as pd
from django.conf import settings
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter
from pm4py.objects.log.importer.xes import importer
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.util.xes_constants import DEFAULT_TIMESTAMP_KEY, DEFAULT_NAME_KEY

# CONSTANTS
from partial_order.general_functions import get_selected_file_path, get_export_file_path

GROUP = 'group'
GROUPS = 'groups'
EVENTS = 'events'
CASEIDS = 'caseIds'
DELAY = 'delay'

pd.options.mode.chained_assignment = None  # default='warn'


"""
Returns the event log as a dataframe object, sorted by timestamps
"""


def get_log():
    parameters = {"timestamp_sort": True}
    event_log = settings.EVENT_LOG
    df = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME, parameters=parameters)
    return df


"""
Write the event log dataframe to a xes file
"""


def write_to_xes(event_log_df):
    event_log_df.replace(np.nan, '', inplace=True)
    event_log = log_converter.apply(event_log_df, variant=log_converter.Variants.TO_EVENT_LOG)
    settings.EVENT_LOG = event_log
    if settings.EVENT_LOG_NAME.endswith('.modified.xes'):
        exporter.apply(event_log, get_selected_file_path())
    else:
        exporter.apply(event_log, get_export_file_path())


"""
Deletes the group information from the groups file and then writes the new timestamps into the log file
"""


def save_delay_to_log(variant_dict):

    event_log_df = get_log()

    # proceed only if the selected variant's group is present in the groups file
    if variant_dict[GROUP] in settings.GROUPS[GROUPS] and variant_dict[DELAY] > 0:
        # save the delay from the user
        time_delay = variant_dict[DELAY]

        # store the sequence in which the events take place
        sequence = variant_dict[EVENTS]

        # sort the variant's group's caseIds in ascending order
        variant_dict[CASEIDS] = sorted(variant_dict[CASEIDS])

        # iterate over each caseId present in the selected group
        for caseId in variant_dict[CASEIDS]:

            # create a sub data frame for the current caseId
            case_df = event_log_df.loc[event_log_df[CASE_CONCEPT_NAME] == caseId]

            # counter for delta modifier
            counter = 0

            # list to store all new timestamps
            new_time_list = list()

            # number of events in each trace
            num_events = len(sequence)

            index = event_log_df[event_log_df[CASE_CONCEPT_NAME] == caseId].index

            # iterate over the  the log to reorder the rows in event_log_df in the order that the user has selected
            idx = 0
            while idx < num_events:
                event_log_df.at[index[idx], event_log_df.columns] = \
                    case_df[case_df[DEFAULT_NAME_KEY] == sequence[idx]].iloc[0].values

                if len(case_df[case_df[DEFAULT_NAME_KEY] == sequence[idx]]) > 1:
                    case_df.loc[case_df[DEFAULT_NAME_KEY] == sequence[idx]] = \
                        case_df.loc[case_df[DEFAULT_NAME_KEY] == sequence[idx]].iloc[1:]
                else:
                    case_df.drop(case_df[case_df[DEFAULT_NAME_KEY] == sequence[idx]].index, inplace=True)

                idx += 1

            # store the timestamps in a list
            timestamps = event_log_df.loc[event_log_df[CASE_CONCEPT_NAME] == caseId][DEFAULT_TIMESTAMP_KEY].tolist()

            # append the first timestamp to the list of new timestamps
            new_time_list.append(timestamps[0])

            # the smallest variant will be 2 events
            # therefore, the smallest possible value for the first duplicate timestamp is 1
            partial_ind = 1

            # find the index of the first duplicate timestamp in the list of timestamps
            while not timestamps[partial_ind] == timestamps[partial_ind - 1]:
                new_time_list.append(timestamps[partial_ind])
                partial_ind += 1

            # iterate over each timestamp in the list of timestamps and then add the corresponding delay
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
        del settings.GROUPS[GROUPS][variant_dict[GROUP]]

        # write event log to the modified xes file
        write_to_xes(event_log_df)
