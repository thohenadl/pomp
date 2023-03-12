import os
import tkinter as tk
import warnings
import sys
import argparse

import pandas as pd


from classes.MyGUI import MyGUI
import classes.userInteraction as ui

from util.csvUtil import log_converter, find_file, prepare_log
from const import *
from util.tagging import *
warnings.simplefilter('ignore')


def showGui():
    gui = MyGUI()
    gui.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = '''Tool for tagging an user interaction log with POMP categories''',
        epilog      = """For more information see source code comments."""
    )
    parser.add_argument('filename')   
    args = parser.parse_args()

    print("*************************")
    print("New execution started \n")

    # ToDo: Create UI To generate POMP Tagged File into Folder pomp_tagged_dir from const.py
    # showGui()

    # (1) Read tagged actions & clean for context only
    tagged_file = find_file(sys.argv[1], path_to_files + "\\" +  pomp_tagged_dir)
    df_tagged_log = prepare_log(tagged_file,0,";")
    
    # (2) Get all columns that are not specified in the context constant
    context_attributes = context_attributes_smartRPA + context_attributes_ActionLogger
    context_attributes_wPOMP = context_attributes + ["pomp_dim"]

    df_tagged_log_context = get_col_filtered_df(df_tagged_log,context_attributes_wPOMP)

    # (3) Addes unique user interaction that were gathered from the tagged file to a set
    tagged_ui_set = generate_unique_UI_set(df_tagged_log_context)

    # (4) Read un-tagged log & clean for context data only
    # (4.0) Add column if not exists: pomp_dim
    # (4.1) Iterate over un-tagged log and tag
    # (4.1a) If a tagged UI exists than tag pomp_dim
    # (4.1b) If no tagged UI exists, than add to untagged_UI Set
    # (4.2) Store File in output folder from const.py  
    
    untagged_ui = set()
    newly_tagged = set()
    lenth_file = -1
    # Get all files in folder
    for (dir_path, dir_names, filenames) in os.walk(path_to_files + "/" + log_dir):
        # Iterate over files in folder that should be tagged
        for filename in filenames:
            # Prepare File
            df_file = prepare_log(filename,1,";")
            # Filter on context attributes
            df_context_file = get_col_filtered_df(df_file,context_attributes)
            lenth_file = len(df_context_file)
            # Add pomp_dim Column to original df if not existend in file
            if 'pomp_dim' not in df_file.columns:
                df_file['pomp_dim'] = ""
            # To Do: Remove iloc to get complete array
            for index, row in df_context_file.iloc[:].iterrows():
                # Create a UI from the row in the dataframe
                row_df = row.to_frame().T
                userInteraction = ui.userInteraction(row_df)
                print(userInteraction)
                # Check if the userInteraction exists in the set
                # issue: https://github.com/thohenadl/pomp/issues/2
                # Compares two User Interactions only on the context_attributes
                # ToDo: Compare Method always returns false at the moment
                match = next((x for x in tagged_ui_set if x.compare_columns(userInteraction,context_attributes)), None)
                if match is None: 
                    print("Has no match in labeled: " + str(userInteraction))
                    untagged_ui.add(userInteraction)
                else:
                    newly_tagged.add(userInteraction)
                    # ToDo does return none at the moment
                    print("Pomp Dim is " + match.get_attribute("pompDim"))
                print("********** Index: " + str(index) + " ************")
    
    print(len(untagged_ui))
    print(len(newly_tagged))
    print(lenth_file)