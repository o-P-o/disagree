import pandas as pd
import numpy as np

def count_nans(lst):
    # Count the number of NaNs in a list.
    num_nans = 0
    null_list = list(pd.isnull(lst))
    for is_null in null_list:
        if is_null:
            num_nans += 1

    return num_nans

def append_one_nan(old_lst, new_lst):
    old_null_list = list(pd.isnull(old_lst))
    for i in range(len(old_null_list)):
        is_null = old_null_list[i]
        if is_null:
            new_lst.append(old_lst[i])
            break

    return new_lst

def flexible_data(df):
    '''
    Input: Dataframe with n(i, j) = j-th annotation for the i-th data instance.
    Output: numbered_labels, list of unique data points converted to numbers
            data_dict, dictionary connecting the original data point to its
                    converted number
    '''
    all_data = [] # Generate a list of every label
    for idx, row in df.iterrows():
        all_data += list(row)

    unique_data = list(set(all_data)) # Reduce it down to a set
    num_nans = count_nans(unique_data) # Should be 1 or 2 (NoneType or NaN)

    unique_data_ex_none = []
    unique_data_nulls = list(pd.isnull(unique_data))
    for i in range(len(unique_data)):
        is_null = unique_data_nulls[i]
        if not is_null:
            unique_data_ex_none.append(unique_data[i])

    new_unique = unique_data_ex_none + [None]
    numbered_labels = [i for i in range(len(unique_data_ex_none))]

    data_dict = { }
    for name, i in zip(new_unique, numbered_labels):
        data_dict[name] = int(i)

    data_dict[None] = None

    return data_dict, numbered_labels

def convert_dataframe(df):
    """
    Input: df, with n(i,j)=jth annotation for ith data point
    Output: new_data, dataframe with inputs updated to numbers indexed from zero
            numbered_labels, list of integer labels from 0
            data_dict, dict converting original labels to new integer labels
    """
    data_dict, numbered_labels = flexible_data(df)

    new_data = { }
    for idx, col in df.iteritems():
        new_col = []
        isnull_col = list(pd.isnull(col))
        for i in range(len(col)):
            isnull = isnull_col[i]
            if isnull:
                new_col = new_col + [None]
            else:
                new_col.append(data_dict[col[i]])
        new_data[idx] = new_col

    new_data = pd.DataFrame(new_data)

    return new_data, numbered_labels, data_dict
