# Import generic Python libraries
import csv
from collections import defaultdict
import os
import pandas as pd
import time
from const import overhead_columns, context_attributes_all
from util.tagging import generate_stats_unique_UI_set, get_col_filtered_df

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
    """
    # Initialize a set to hold unique rows across all files
    unique_rows = set()
    total_rows = 0
    files = 0
    start_time = time.time()
    unique_uis = set()
    context_attributes_wPOMP = context_attributes_all + ["pomp_dim"]

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        print(filename + " started.")
        if filename.endswith('.csv'):
            files += 1
            # Read the CSV file into a pandas dataframe
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, index_col=0)
            # df = df.drop(columns=to_drop)
            total_rows += len(df)

            with open(os.path.join(folder_path, filename), newline='') as f:
                reader = csv.reader(f)
                header = next(reader)
                indices_to_exclude = [header.index(col) for col in overhead_columns if col in header]
                for row in reader:
                    unique_row = tuple([row[i] for i in range(len(row)) if i not in indices_to_exclude])
                    unique_rows.add(unique_row)

            df = get_col_filtered_df(df,context_attributes_wPOMP)
            # Create Unique UIs for all CSV files processed
            unique_uis = generate_stats_unique_UI_set(df,unique_uis)

        print(filename + " contains " + str(len(df)) + " rows.")
        print("So far, there are " + str(len(unique_rows)) + " unique rows.")
        print("So far, there are " + str(len(unique_uis)) + " unique user interactions.")
        time.sleep(3)

    end_time = time.time()
    tdelta = end_time - start_time
    print("File processing complete")
    # Print the total number of unique rows
    print(folder_path + " contains " + str(total_rows) + " rows in " + str(files) + " files.")
    print("There are " + str(len(unique_rows)) + " unique rows so far.")
    print("There are " + str(len(unique_uis)) + " unique user interactions so far.")
    print("\nExecution time: " +  str(round(tdelta,3)) + " seconds.")

    return unique_uis