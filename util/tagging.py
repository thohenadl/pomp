# Import Constants
from const import action_Dimensions, context_attributes_ActionLogger, context_attributes_smartRPA

# Import Classes
import classes.userInteraction

# Import Util
from util.csvUtil import *
from const import *

# Import necessary libaries
import pandas as pd

def generate_unique_UI_set(log: pd.DataFrame) -> set:
    """
    The function generate_unique_UI_set takes a Pandas DataFrame log as input and 
        returns a set containing unique instances of userInteraction objects created 
        from the rows of the input DataFrame.
    Note: This function drops any columns that are not required for creating a 
        userInteraction object. Also, if a userInteraction object with the same attribute
        values already exists in the set, it will not be added again.
    
    Args:
        log (Pandas DataFrame): The input DataFrame containing data to create userInteraction objects from.
    
    Returns:
        unique_UI_set (Set): A set of unique instances of userInteraction objects.
    """
    unique_UI_set = set()
    for index, row in log.iterrows():
        # Create a dataframe from the row, which is added to the userInteraction
        row_df = row.to_frame().T

        # Create a new user Interaction
        row_UI = ui.userInteraction(row_df)
        
        # Check if User Interaction is already in unique set and if add to set
        if row_UI not in unique_UI_set:
            # print("Added " + str(row_UI))
            unique_UI_set.add(row_UI)

    # Return set of unique user interactions
    return unique_UI_set

# Iterate over un-tagged log
def tag_UI_w_POMP(tagged_filename: str):
    """
    Takes in two user interaction log files: one tagged with an attribute POMP and another 
        without tags. The first file is scanned for unique user interactions and their 
        POMP tag. These actions are added to a set. Afterwards, the second given file is
        looped and each row is tagged based on the tags from the first file.

    Args:
        tagged_filename: File that has the Tags for POMP set in POMP Folder

    Returns:
        Nothing

    Creates:
        POMP-Dimension Column for all files in uilogs folder
    """
    # (1) Read tagged actions & clean for context only
    tagged_file = find_file(tagged_filename, path_to_files + "\\" +  pomp_tagged_dir)
    df_tagged_log = prepare_log(tagged_file,0,seperator)
    
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
            df_file = prepare_log(filename,1,seperator)
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
                # Check if the userInteraction exists in the set
                # issue: https://github.com/thohenadl/pomp/issues/2
                # Compares two User Interactions only on the context_attributes
                # ToDo: Compare Method always returns false at the moment
                match = next((x for x in tagged_ui_set if x.compare_columns(userInteraction,context_attributes)), None)
                if match is None: 
                    # print("Has no match in labeled: " + str(userInteraction))
                    untagged_ui.add(userInteraction)
                else:
                    newly_tagged.add(userInteraction)
                    # ToDo does return none at the moment
                    # print("Pomp Dim is " + match.get_attribute("pompDim"))
                    df_file.loc[index,'pomp_dim'] = match.get_attribute("pompDim")
                print("********** Index: " + str(index) + " ************")
            print(df_file)
            # To Do: Store df_file
    
    print(len(untagged_ui))
    print(len(newly_tagged))
    print(lenth_file)
    
    return True


# Append Empty Actions to Tagged File
def append_Empty():
    # Each unique untagged row will be added to initial tagged file for manual processing
    str("something")

# Store files
