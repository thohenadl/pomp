import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter


def load_and_convert_to_log(path, case, timestamp, sep):
    log_csv = read_csv(path, sep)
    log_csv = log_csv.sort_values(timestamp)
    event_log = log_converter.apply(log_csv,parameters={log_converter.to_event_log.Parameters.CASE_ID_KEY: case})
    return event_log


def read_csv(path, sep):
    try:
        log_csv = pd.read_csv(path, sep=sep)
    except UnicodeDecodeError:
        log_csv = pd.read_csv(path, sep=sep, encoding="ISO-8859-1")
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    return log_csv


def load_and_convert_to_df(log):
    return log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
