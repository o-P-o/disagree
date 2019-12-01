import pandas as pd

def move_to_end(lst):
    new_list = [label for label in lst if label]

    return new_list + [None]

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
    unique_data = move_to_end(unique_data)
    unique_data_ex_none = list(filter(None, unique_data))

    numbered_labels = [i for i in range(len(unique_data_ex_none))]

    data_dict = { }
    for name, i in zip(unique_data, numbered_labels):
        data_dict[name] = float(i)

    data_dict[None] = None

    return data_dict, numbered_labels

def convert_dataframe(df):
    data_dict, numbered_labels = flexible_data(df)

    new_data = { }
    for idx, col in df.iteritems():
        new_column = []
        for instance in col:
            new_column.append(data_dict[instance])
        new_data[idx] = new_column

    new_data = pd.DataFrame(new_data)

    return new_data, numbered_labels, data_dict
