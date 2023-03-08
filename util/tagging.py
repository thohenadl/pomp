# Import Constants
from const import action_Dimensions, context_attributes_ActionLogger, context_attributes_smartRPA

# Import Classes
import classes.userInteraction

# Import Util
from util.csvUtil import *
from const import TERMS_FOR_MISSING
import classes.userInteraction as ui

# Import necessary libaries
import pandas as pd

def get_context_parameters_df(log: pd.DataFrame, context_attributes: list) -> pd.DataFrame:
    """
    Remove context attributes from Datafrae

    Args:
        log (DataFrame): DataFrame that should be cleaned
        context_attributes (List): String List of column names to be kept

    Returns:
        df_stripped (DataFrame): Returns DataFrame with columns specified 
    
    """
    # Fixes Drop was tested, did not work due to "not in list error"
    # https://github.com/thohenadl/pomp/issues/1
    new_col_list = [col for col in context_attributes if col in log.columns]
    df_stripped = log[new_col_list]
    return df_stripped

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
        
        #Create a new user Interaction
        row_UI = make_UI(row_df)

        # Check if User Interaction is already in unique set and if add to set
        if row_UI not in unique_UI_set:
            # print("Added " + str(row_UI))
            unique_UI_set.add(row_UI)

    # Return set of unique user interactions
    return unique_UI_set

def make_UI(row: pd.DataFrame) -> classes.userInteraction:
    """
    Makes an user interaction class object from a dataframe row
    
    Args:
        row (DataFrame): A row of a user interaction log in DataFrame format
        
    Returns:
        action (UserInteraction): A user interaction class object
    """
    action = ui.userInteraction(row)

    # Check if the DataFrame has the pomp_dim tag as column and if add to UI
    if 'pomp_dim' in row.columns:
        action.set_attribute("pompDim",row["pomp_dim"].iloc[0])

    # Check if User Interaction is already in unique set and if add to set

    return action

# Iterate over un-tagged log
def tag_UI_w_POMP(df_untagged: pd.DataFrame, set_tagged_UI: set) -> pd.DataFrame:

    # Get Class per row

    # Get Tag per row

    # Set Tag per row

    # return log
    return 

# Append Empty Actions to Tagged File
def append_Empty():
    # Each unique untagged row will be added to initial tagged file for manual processing
    str("something")

# Store files
