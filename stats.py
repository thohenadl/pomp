# Import generic Python libraries
import argparse
import pandas as pd
import sys

# Import project specific
import util.csvUtil
from util.statsUtil import *
from const import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = '''Getting Metrics from Log files
            If a filepath is provided, there will only be a CSV file created.''',
        epilog      = """For more information see source code comments."""
    )
    # parser.add_argument('filename')   
    parser.add_argument("-f", "--filepath", help="Path to file", type=str)
    args = parser.parse_args()
    filepath = args.filepath

    # Namevalues for the file to be stored
    datetime = time.strftime("%Y%m%d-%H%M%S")
    untagged_filename = "untaggedUI-" + datetime

    if filepath is None:
        total_rows_count, total_files_count, unique_rows, unique_uis = stats(path_to_untagged)
        # Store the untagged UIs set into the project
        store_set(unique_uis,untagged_filename, 1)
        # Save some stats to an XML file
        save_data_to_xml(untagged_filename, total_rows_count, total_files_count, unique_rows)
    else: 
        loaded_pickled = load_pickled(filepath)
        store_set(loaded_pickled,untagged_filename,False)
        print("File procssed - CSV available")

    sys.exit()