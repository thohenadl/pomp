import pandas as pd
import os
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def load_and_convert_to_log(path, case, timestamp, sep):
    log_csv = read_csv(path, sep)
    log_csv = log_csv.sort_values(timestamp)
    event_log = log_converter.apply(log_csv,parameters={log_converter.to_event_log.Parameters.CASE_ID_KEY: case})
    return event_log


def read_csv(path, sep):
    try:
        log_csv = pd.read_csv(path, sep=sep)
    except UnicodeDecodeError:
        log_csv = pd.read_csv(path, sep=sep, encoding="ISO-8859-1")
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    return log_csv


def load_and_convert_to_df(log):
    return log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)


def find_file(filename: str, folder_path: str) -> str:
    """
    Searches for a file with the given name in the given folder and returns the full path to the file.

    Args:
        filename (str): The name of the file to search for.
        folder_path (str): The path to the folder to search in.

    Returns:
        str: The full path to the file, or an empty string if the file was not found.
    """
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Loop over the file list and check each file name
    for file in file_list:
        if os.path.splitext(file)[0] == filename:
            # If the file is found, return the full path
            return file

    # If the file was not found, return an empty string
    raise FileNotFoundError("POMP Tagged File not found! \n File-folder ")

