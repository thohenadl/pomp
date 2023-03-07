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

    print("*************************")
    print("New execution started \n")

    # ToDo: Create UI To generate POMP Tagged File into Folder pomp_tagged_dir from const.py

    # (1) Read tagged actions & clean for context only
    tagged_file = find_file(sys.argv[1], path_to_files + "\\" +  pomp_tagged_dir)
    df_tagged_log = prepare_log(tagged_file,0,";")
    
    # (2) Get all columns that are not specified in the context constant
    context_attributes = context_attributes_smartRPA + context_attributes_ActionLogger
    context_attributes_wPOMP = context_attributes + ["pomp_Dim"]
    
    df_tagged_log_context = get_context_parameters_df(df_tagged_log,context_attributes_wPOMP)

    # (3) Addes unique user interaction that were gathered from the tagged file to a set
    tagged_ui_set = generate_unique_UI_set(df_tagged_log_context)
    print(tagged_ui_set)

    # (4) Read un-tagged log & clean for context data only
    # (4.0) Add column if not exists: pomp_dim
    # (4.1) Iterate over un-tagged log and tag
    # (4.1a) If a tagged UI exists than tag pomp_dim
    # (4.1b) If no tagged UI exists, than add to untagged_UI Set
    # (4.2) Store File in output folder from const.py  
    
    untagged_ui = set()
    for (dir_path, dir_names, filenames) in os.walk(path_to_files + "/" + log_dir):
        for filename in filenames:
            df_file = prepare_log(filename,1,";")
            df_context_file = get_context_parameters_df(df_file,context_attributes)
            # Add pomp_dim Column if not existend in fie
            if 'pomp_dim' not in df_context_file.columns:
                df_context_file['pomp_dim'] = ""
            for index, row in df_context_file.iterrows():
                # Create a UI from the row in the dataframe
                row_df = row.to_frame().T
                userInteraction = make_UI(row_df)
                # Check if the userInteraction exists in the set
                match = next((x for x in tagged_ui_set if x == userInteraction), None)
                print(match)

    

      
