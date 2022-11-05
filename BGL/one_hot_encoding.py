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


def one_hot_encode_list_input(input_df: pd.DataFrame, col_name: str):
    col_name_as_list = col_name + '_list'
    input_df[col_name_as_list] = input_df[col_name].apply(lambda x: sanitize_tags(x))  # convert to list the typecasted input
    binarizer = MultiLabelBinarizer().fit(input_df[col_name_as_list])
    vector_df = pd.DataFrame(binarizer.transform(input_df[col_name_as_list]), columns=binarizer.classes_)
    vector_df.columns = [col_name + "_" + col for col in vector_df.columns]
    vector_df.loc[:, "submission_id"] = input_df['submission_id']
    vector_df = vector_df.set_index('submission_id')
    return vector_df

def sanitize_tags(tags, ignore_nans_and_empty=False):
    """
    Cleans up a multiple choice string

    # copied from https://github.com/Streetbees/data-lib/blob/master/streetbees_data/utils/strings.py
    # due to dependency issues

    Parameters
    ----------
    tags : string
         Multiple choice string
    ignore_nans_and_empty: boolean
         whether to ignore nans and empty strings
    Returns
    -------
    list
        list of cleaned up tags
    """
    if not tags:
        return None
    if isinstance(tags, float):
        if not pd.isna(tags) and int(tags) == tags:
            tags = int(tags)
    if ignore_nans_and_empty and pd.isna(tags):
        tags = ""
    tags = str(tags)
    if ignore_nans_and_empty and (tags == ""):
        tags_list = []
    else:
        tags_list = tags.split('",')
    tags_clean = [
        "".join(
            [
                x
                for x in tag
                if x in string.ascii_letters + "1234567890'- _/,.&<>()?!+$£+:%ü’“”"
            ]
        ).strip()
        for tag in tags_list
    ]
    return tags_clean