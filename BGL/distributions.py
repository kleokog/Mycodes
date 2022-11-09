import pandas as pd

def weighted_count(df, column, weight_column, mode='Count'):
    """
    Returns a weighted sum of the elements in df[column].
    Note that df[column] needs to be a series of lists

    :param df: dataframe to count
    :param column: column containing lists whose entries need to be counted
    :param weight_column: column containing weights for each row
    :param mode: type of aggregation.
    :return:
    """
    if not df[column].apply(lambda x: isinstance(x, list)).all():
        raise TypeError(f"Please make sure the column {column} contains lists only.")
    if mode == 'Count':
        total_weight = df[weight_column].sum()
        return (
            df
            [[column, weight_column]]
            .explode(column)
            .groupby(column)
            [weight_column]
            .sum()
            .div(total_weight)
            .rename("ALL")
        )
    else:
        raise AttributeError("The selected mode is not available.")


def create_distribution(df: pd.DataFrame,
                        pivot_by: str,
                        coded_question: str,
                        weight_col: str = 'weights_column',
                        question_label: str = 'Answers'):
    """
    This function will take a data sheet, submission re-mapping and a coded question to return a dataframe
    containing the question, the list of possible answers, the distribution of of each cluster's answers
    and the distribution of the total responses for each answer.

    """
    assert ~df[coded_question].isna().any(), f"Please make sure the {coded_question} columns contains no nulls."

    # get sample sizes
    sample_dist = str(
        df
        .loc[lambda x: x[coded_question].notnull()]
        .groupby(pivot_by)
        [weight_col]
        .sum()
        .to_dict()
    )

    data = df.copy()
    data[question_label] = data[coded_question].apply(sanitize_tags)

    full_count = weighted_count(data, question_label, weight_col, 'Count')

    dummy_df = data[question_label].str.join(sep='*').str.get_dummies(sep='*').multiply(data[weight_col], axis=0)
    data = (
        data
        [[pivot_by, weight_col]]
        .join(dummy_df)
    )
    # get size of different target column
    cluster_size = data.groupby(pivot_by)[weight_col].sum()

    output = (
        data
        .groupby(by=[pivot_by])
        [dummy_df.columns]
        .sum()
        .divide(cluster_size, 0)
        .rename_axis(question_label, axis=1)
        .T
        .join(full_count)
        .reset_index()
    )

    # adding the sample and question as constant at the beginning of the dataframe for excel export.
    output.insert(loc=0, column='question', value=coded_question)
    output.insert(0, column='sample', value=sample_dist)

    return output