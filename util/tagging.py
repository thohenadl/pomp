# Import Constants
from const import action_Dimensions, context_attributes_ActionLogger, context_attributes_smartRPA

# Import Classes
import classes.userInteraction

# Import Util
from util.csvUtil import *

# Import necessary libaries
import pandas as pd


# Read tagged actions & clean for context only
def read_tagged_UIs(filename):
    concat_ContextParam = context_attributes_ActionLogger + context_attributes_smartRPA
    tagged_UIs = read_csv_and_filter_columns(filename, concat_ContextParam)
# Generate UI classes

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
