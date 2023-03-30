import tkinter as tk
import warnings
import argparse

import pandas as pd

from classes.MyGUI import MyGUI
import classes.userInteraction as ui

warnings.simplefilter('ignore')

def showGui():
    gui = MyGUI()
    gui.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = '''Tool for tagging an user interaction log with POMP categories''',
        epilog      = """For more information see source code comments."""
    )
    # parser.add_argument('filename')   
    args = parser.parse_args()

    print("*************************")
    print("New execution started \n")

    showGui()
