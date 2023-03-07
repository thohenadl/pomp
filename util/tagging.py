# Import Constants
from const import action_Dimensions, context_attributes_ActionLogger, context_attributes_smartRPA

# Import Classes
import classes.userInteraction

# Import Util
from util.csvUtil import *
from const import TERMS_FOR_MISSING

# Import necessary libaries
import pandas as pd


# Generate UI classes
def create_value_tup(row):
    tup = []
    for att in row:
        if str(row[att]) not in TERMS_FOR_MISSING:
            tup.append(str(row[att]))
    return tup


# Read un-tagged log & clean for context data only

# Iterate over un-tagged log
def tag_POMP():
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
