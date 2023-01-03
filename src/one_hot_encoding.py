import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

def join_to_df(df_to_add:pd.DataFrame, complete_df:pd.DataFrame):
    '''
    Parameters
    ----------
    df_to_add: is the new data that we want to add to complete_df
    complete_df: complete_df is the full dataframe, the one that we want to return
    Returns
    -------
    '''
    try:
        complete_df
    except:
        print("target dataframe does not exist, initialising an empty dataframe")
        complete_df = pd.DataFrame()
    if complete_df.empty:
        complete_df = df_to_add
    else:
        complete_df = complete_df.join(df_to_add)
    return complete_df


def encode_categorical_variable(input_df:pd.DataFrame, col_name:str, id_col:str):
    '''
    Returns
    -------
    Returns one-hot-encoded dataframe of a column. This function should be applied only to columns where the input is
    not a list but a single value
    '''
    dummy_df = pd.get_dummies(input_df[col_name], prefix=col_name)
    dummy_df[id_col] = input_df[id_col]
    dummy_df = dummy_df.set_index(id_col)
    return dummy_df

