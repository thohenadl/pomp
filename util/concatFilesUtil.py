# Just a file to concat multiple user interaction log recordings into a single recording

import os
import pandas as pd

def read_multiple_csv_files(file_path: str) -> pd.DataFrame:
    # Initialize an empty dataframe to store the combined data
    combined_data = pd.DataFrame()
    
    # Get a list of all CSV files in the specified directory
    csv_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.csv')]

    # Loop through each file and read it into a dataframe
    for csv_file in csv_files:
        # Read the CSV file into a dataframe
        data = pd.read_csv(csv_file)
        
        # Add a new column to the dataframe with the filename as the case_id
        # Necessary if the case name can be redundant per file, but the file name is unique (datetime)
        # filename = os.path.splitext(os.path.basename(csv_file))[0]
        # data['case:concept:name'] = data['case:concept:name'].apply(lambda x: f"{filename}_{x}")
        
        # Concat the data to the combined dataframe
        combined_data = pd.concat([combined_data,data], ignore_index=True)
    
    return combined_data