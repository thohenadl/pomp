import os
import tkinter as tk
import warnings

import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from classes.MyGUI import MyGUI
import classes.userInteraction

from util.csv import log_converter
from const import *
warnings.simplefilter('ignore')


def prepare_log(log_name, parse_dates=False):
    if ".xes" in log_name:
        log1 = xes_importer.apply(os.path.join(path_to_files, log_dir, log_name))
        frame = log_converter.apply(log1, variant=log_converter.Variants.TO_DATA_FRAME)
        frame = frame.reset_index()
    else:
        frame = pd.read_csv(path_to_files + "/" + log_dir + "/" + log_name, sep=",", quotechar='"', engine="python",
                            error_bad_lines=False, parse_dates=parse_dates)
    return frame

def showGui(filename):
    gui = MyGUI(filename)
    gui.run()

if __name__ == "__main__":
    for (dir_path, dir_names, filenames) in os.walk(path_to_files + "/" + log_dir):
        for filename in filenames:
            showGui(filename)

    