import os
import tkinter as tk
import warnings
import sys
import argparse

import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from classes.MyGUI import MyGUI
import classes.userInteraction as ui

from util.csvUtil import log_converter, find_file
from const import *
from util.tagging import *
warnings.simplefilter('ignore')


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
        frame = pd.read_csv(path_to_files + "/" + directory + "/" + log_name, sep=seperator, quotechar='"', engine="python", error_bad_lines=False, parse_dates=parse_dates)
    return frame

def showGui(filename):
    gui = MyGUI(filename)
    gui.run()

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Tool vtagging an user interaction log with POMP categories''',
        epilog="""For more information see source code comments.""")
    parser.add_argument('Tagged Log', type=str, default="", help='Log tagged with POMP Categories')
    args=parser.parse_args()

    # Read tagged actions & clean for context only
    tagged_file = find_file(sys.argv[1], path_to_files + "\\" +  pomp_tagged_dir)
    df_tagged_log = prepare_log(tagged_file,0,";")
    
    # Get all columns that are not specified in the context constant
    context_attributes = context_attributes_smartRPA + context_attributes_ActionLogger
    
    # Remove context attributes from file
    # Drop was tested, did not work due to "not in list error"
    # https://github.com/thohenadl/pomp/issues/1
    new_col_list = [col for col in context_attributes if col in df_tagged_log.columns]
    df_tagged_log_context = df_tagged_log[new_col_list]

    print(df_tagged_log_context)
    # Create unique UI repository
    ui_set = set()

    row_1 = ui.userInteraction(df_tagged_log_context.iloc[22].to_frame().T)
    row_2 = ui.userInteraction(df_tagged_log_context.iloc[23].to_frame().T)
    ui_set.add(row_1)
    print(row_1 in ui_set)
    print(row_2 in ui_set)
    print(row_1 == row_2)

    # for index, row in df_tagged_log_context.iterrows():
    #     row_df = row.to_frame().T
    #     row_UI = ui.userInteraction(row_df)
    #     print(row_UI.get_attribute("context_fields_str"))
    #     if row_UI not in ui_set:
    #         print("Added " + str(row_UI))
    #         ui_set.add(row_UI)

    print(len(ui_set))
    print(ui_set)

    # Read un-tagged log & clean for context data only
    for (dir_path, dir_names, filenames) in os.walk(path_to_files + "/" + log_dir):
        for filename in filenames:
            print(filename)


    # Iterate over un-tagged log

    # Append Empty Actions to Tagged File

    # Store files        
