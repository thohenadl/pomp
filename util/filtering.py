import pandas as pd

def get_col_filtered_df(log: pd.DataFrame, context_attributes: list) -> pd.DataFrame:
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