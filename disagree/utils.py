import pandas as pd
import numpy as np
import math

def move_to_end(lst):
    # If there is a None in the list, move to the end. If there is a NaN
    # then replace with None and move to the end.
    new_list = []
    for label in lst:
        if float(label) == 0.0:
            new_list.append(0.0)
        if label and not math.isnan(label):
            new_list.append(label)

    return new_list + [None]

def count_nans(lst):
    # Count the number of NaNs in a list.
    num_nans = 0
    for x in lst:
        if math.isnan(x):
            num_nans += 1

    return num_nans

def append_one_nan(old_lst, new_lst):
    for x in old_lst:
        if math.isnan(x):
            new_lst.append(x)
            break

    return new_lst

def flexible_data(df):
    '''
    Input: Dataframe with n(i, j) = j-th annotation for the i-th data instance.
    Output: numbered_labels, list of unique data points converted to numbers
            data_dict, dictionary connecting the original data point to its
                    converted number
    '''
    all_data = []
    for idx, row in df.iterrows():
        all_data += list(row)

    unique_data = list(set(all_data))
    num_nans = count_nans(unique_data)

    new_unique = []
    for dat in unique_data:
        if not math.isnan(dat):
            new_unique.append(dat)
    if num_nans > 0:
        new_unique = append_one_nan(unique_data, new_unique)

    new_unique = move_to_end(new_unique)
    unique_data_ex_none = list(filter(lambda x: x is not None, new_unique))
    numbered_labels = [i for i in range(len(unique_data_ex_none))]

    data_dict = { }
    for name, i in zip(new_unique, numbered_labels):
        data_dict[name] = float(i)

    data_dict[None] = None

    return data_dict, numbered_labels

def convert_dataframe(df):
    data_dict, numbered_labels = flexible_data(df)

    new_data = { }
    for idx, col in df.iteritems():
        new_column = []
        for instance in col:
            if math.isnan(instance):
                new_column.append(data_dict[None])
            else:
                new_column.append(data_dict[instance])
        new_data[idx] = new_column

    new_data = pd.DataFrame(new_data)

    return new_data, numbered_labels, data_dict
