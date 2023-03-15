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
        description = '''Tool vtagging an user interaction log with POMP categories''',
        epilog      = """For more information see source code comments."""
    )
    args = parser.parse_args()


    print("*************************")
    print("New execution started \n")

    # ToDo: Create UI To generate POMP Tagged File into Folder pomp_tagged_dir from const.py
    # showGui()

    # Tagges a single file with the POMP tags from the POMP Tagged folder file
    # Hard Coded for now
    tagged_file = "pompTagged"
    tag_UI_w_POMP(tagged_file)

      
