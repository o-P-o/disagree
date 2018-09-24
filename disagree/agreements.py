"""
See Jupyter notebooks for example usage
"""
import numpy as np
import pandas as pd
import sys
import math
import itertools


DATAFRAME_ERROR = "Data input must be a pandas DataFrame"
DATAFRAME_TYPES_ERROR = "DataFrame entries must be int types, float types, or NaN"
LABELS_TYPE_ERROR = "Argument 2 must be of type list"
LABELS_ELEMENTS_TYPE_ERROR = "All elements in list of labels must be of type int"


def main_input_checks(df, labels):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(DATAFRAME_ERROR)

    for type_ in df.dtypes:
        if not (type_ == int or type_ == float):
            raise TypeError(DATAFRAME_TYPES_ERROR)

    if not isinstance(labels, list):
        raise TypeError(LABELS_TYPE_ERROR)

    if not all(isinstance(n, int) for n in labels):
        raise TypeError(LABELS_ELEMENTS_TYPE_ERROR)


class BiDisagreements():
    """
    Used for assessing absolute disagreements from manual annotations, with the
    ability to visualise bidisagreements, and see values of other disagreement
    quantities.
    """
    def __init__(self, df, labels):
        """
        Parameters
        ----------
        annotator_labels: pandas dataframe, required
            Columns indexed by annotator name; rows indexed by labelled instance
        labels: list, required
            List of all the possible labels
            e.g. [label1, label2, label3, ... ]
        """
        main_input_checks(df, labels)

        self.df = df
        self.labels = labels
        n = len(self.labels)
        self.matrix = np.zeros((n, n))
        self.reference_length = self.df.shape[0]

        # Initialise the empty agreements dictionary (good format for access efficiency later)
        # Of the form { label1: {label1: num_disagreements, label2: num_disagreements, ... },
        #               label2: {label1: num_disagreements, label2: num_disagreements, ... }, ... }
        self.agreements_dict = {}
        for label1 in self.labels:
            if label1 not in self.agreements_dict and label1 != None:
                self.agreements_dict[label1] = {}
            else:
                continue
            for label2 in self.labels:
                if label2 not in self.agreements_dict[label1] and label2 != None:
                    self.agreements_dict[label1][label2] = 0

    def agreements_summary(self):
        """
        Prints out all of the return types outlined below.

        Parameters
        ----------
        None

        Returns
        -------
        full_agreement: int
            Number of instances labelled with no disagreements
        bidisagreement: int
            Number of instances labelled with 1 disagreement
        tridisagreement: int
            Number of instances labelled with 2 disagreements
        more: int
            Number of instances labelled with 3 or more disagreements
        """
        full_agreement, bidisagreement, tridisagreement, more = 0, 0, 0, 0
        for idx, row in self.df.iterrows():
            labels = [int(label) for label in row if not math.isnan(label)]
            if len(labels) <= 1: # If no one labelled or if 1 person labelled
                continue
            num_disagreements = len(set(labels))
            if num_disagreements == 1:
                full_agreement += 1
            elif num_disagreements == 2:
                bidisagreement += 1
            elif num_disagreements == 3:
                tridisagreement += 1
            else:
                more += 1

        print("Number of instances with:")
        print("=========================")
        print("No disagreement: " + str(full_agreement))
        print("Bidisagreement: " + str(bidisagreement))
        print("Tridisagreement: " + str(tridisagreement))
        print("More disagreements: " + str(more))

        return full_agreement, bidisagreement, tridisagreement, more

    def dict2matrix(self):
        # Used to convert agreements dictionary to agreements matrix
        dict_ = self.agreements_dict
        for key1 in dict_:
            for key2 in dict_[key1]:
                self.matrix[key1][key2] = dict_[key1][key2]

    def agreements_matrix(self):
        """
        Parameters
        ----------
        None

        Returns
        -------
        agreements_matrix: numpy array
            symmetric matrix of size (len(labels) x len(labels)), showing
            label disagreements between annotators
        """
        for idx, row in self.df.iterrows():
            labels = [int(label) for label in row if not math.isnan(label)]
            k = set(labels)
            if len(k) == 2:
                k = list(k)
                label1 = k[0]
                label2 = k[1]
                self.agreements_dict[label1][label2] += 1
                self.agreements_dict[label2][label1] += 1

        self.dict2matrix()

        return self.matrix
