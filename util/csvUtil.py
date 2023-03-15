import pandas as pd
import os
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

from const import *

def prepare_log(log_name: str, version: int, seperator: str, parse_dates=False) -> pd.DataFrame:
    """
    Prepares a log file and converts .xes or .csv into a Pandas Dataframe

    Args:
        log_name (str): The name of the file to prepare
        version (int): 0 for tagged input, 1 for empty input

    Returns:
        pd.Dataframe: A pandas Dataframe including the read log file
    """
    directory = ""
    if version == 0:
        directory = pomp_tagged_dir
    else:
        directory = log_dir
    if ".xes" in log_name:
        log1 = xes_importer.apply(os.path.join(path_to_files, directory, log_name))
        frame = log_converter.apply(log1, variant=log_converter.Variants.TO_DATA_FRAME)
        frame = frame.reset_index()
    else:
        frame = pd.read_csv(path_to_files + "/" + directory + "/" + log_name, sep=seperator, quotechar='"',encoding="latin-1", engine="python", error_bad_lines=False, parse_dates=parse_dates)
    return frame

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

