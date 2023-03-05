import os
import tkinter as tk
import warnings
import sys
import argparse

import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from classes.MyGUI import MyGUI
import classes.userInteraction

from util.csvUtil import log_converter, find_file
from const import *
warnings.simplefilter('ignore')


def prepare_log(log_name: str, version: int, parse_dates=False) -> pd.DataFrame:
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
        frame = pd.read_csv(path_to_files + "/" + directory + "/" + log_name, sep=",", quotechar='"', engine="python", error_bad_lines=False, parse_dates=parse_dates)
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
    file = find_file(sys.argv[1], path_to_files + "\\" +  pomp_tagged_dir)
    tagged_Log = prepare_log(file,0)
    print(tagged_Log)
    # Read un-tagged log & clean for context data only

    # Iterate over un-tagged log

    # Append Empty Actions to Tagged File

    # Store files        
