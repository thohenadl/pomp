# Import generic Python libraries
import csv
from collections import defaultdict
import os
import pickle
import pandas as pd
import time
import xml.etree.ElementTree as ET

# Imports from Project
from const import overhead_columns, context_attributes_all, uiobjects_dir
from util.tagging import generate_stats_unique_UI_set, get_col_filtered_df, log_from_untagged

def stats(folder_path: str) -> int:
    """
    Reads all CSV files in the specified folder path and returns the total number of rows across all CSV files.
        Counts the total number of unique rows across all CSV files in the given folder.

    Args:
        folder_path (str): Path to the folder containing CSV files.

    Returns:
        int: The total number of rows across all CSV files.
        int: The total number of CSV files processed.
        int: Number of unique rows across all CSV files.
        uiobjects (set): Set of unique User Interactions in folder
    """
    # Initialize a set to hold unique rows across all files
    unique_rows = set()
    total_rows_count = 0
    files_count = 0
    start_time = time.time()
    unique_uis = set()
    context_attributes_wPOMP = context_attributes_all + ["pomp_dim"]

    # Iterate over each file in the folder
    csv_files = (filename for filename in os.listdir(folder_path) if filename.endswith('.csv'))
    for filename in csv_files:
        print(filename + " started.")
        files_count += 1
        # Read the CSV file into a pandas dataframe
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, index_col=0)
        total_rows_count += len(df)

        indices_to_exclude = [col for col in overhead_columns if col in df.columns]
        unique_rows |= set(tuple(row) for row in df.drop(columns=indices_to_exclude).to_records(index=False))

        if len(unique_uis) < 999999999999999999:
            df = get_col_filtered_df(df,context_attributes_wPOMP)
            # Create Unique UIs for all CSV files processed
            unique_uis = generate_stats_unique_UI_set(df,unique_uis)

        print(filename + " contains " + str(len(df)) + " rows.")
        print("So far, there have been " + str(total_rows_count) + " been processed.")
        print("So far, there are " + str(len(unique_rows)) + " unique rows.")
        print("So far, there are " + str(len(unique_uis)) + " unique user interactions.")
        time.sleep(3)

    end_time = time.time()
    tdelta = end_time - start_time
    print("File processing complete")
    # Print the total number of unique rows
    print(folder_path + " contains " + str(total_rows_count) + " rows in " + str(files_count) + " files.")
    print("There are " + str(len(unique_rows)) + " unique rows so far.")
    print("There are " + str(len(unique_uis)) + " unique user interactions so far.")
    print("\nExecution time: " +  str(round(tdelta,3)) + " seconds.")

    return total_rows_count, files_count, len(unique_rows), unique_uis


def store_set(ui_set: set, untagged_filename: str, variant=True) -> None:
    """
    Pickle a set of objects and save to /uiobjects folder and
        creates csv file in the pomp tagged folder

    Parameters:
        ui_set (set): Set of objects to be pickled
        untagged_filename (str: Filename for the pickled file
        variant (Bool): True for Pickle and CSV file, 
            False only for CSV file
            Default: True

    Returns:
        None

    Creates:
        Pickled Dump of UI set
        CSV file with UI set
    """    
    if variant:
        # Check if /uiobjects folder exists, and create it if not
        if not os.path.exists(uiobjects_dir):
            os.mkdir(uiobjects_dir)

        # Pickle the set to a file in /uiobjects folder
        filename = uiobjects_dir + untagged_filename + ".pickle"
        with open(filename, "wb") as f:
            pickle.dump(ui_set, f)
        # This part of thefunction provides a function to load a set of UI Objects
        #     which were generated in the stats.py main. The UI objects
        #     are loaded, read and stored as a csv file into the POMP
        #     Tagged folder. Then the file can be loaded in the main.py
        
    log_from_untagged(ui_set)

def save_data_to_xml(untagged_filename: str, total_rows: int, unique_rows: int, unique_uis: int, files: int) -> None:
    """
    Write three integer values to an XML file located at file_path.

    Args:
        filename (str): Filename of xml file
        total_rows (int): The total row count
        unique_rows (int): The unique row count
        unique_uis (int): The unique user interaction count
        files (int): Number of files processed

    Returns:
        None

    Raises:
        IOError: If there is an error writing to the file.
    """
    root = ET.Element(untagged_filename)
    element_a = ET.SubElement(root, "Total Row Count")
    element_a.text = str(total_rows)
    element_b = ET.SubElement(root, "Unique Row Count")
    element_b.text = str(unique_rows)
    element_c = ET.SubElement(root, "Unique User Interaction Count")
    element_c.text = str(unique_uis)
    element_d = ET.SubElement(root, "Number of files")
    element_d.text = str(files)
    tree = ET.ElementTree(root)
    filename = uiobjects_dir + untagged_filename + ".xml"
    tree.write(filename)

def load_pickled(pickled_file_path: str) -> object:
    """
    Get a pickled file

    Args:
        pickled_file_path (str): Filepath to .pickled file

    Returns:
        The pickled object in the file
    """
    # Load the set from the pickled file
    with open(pickled_file_path, 'rb') as f:
        return  pickle.load(f)