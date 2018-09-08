"""
Example
-------
>>> import pandas as pd
>>> from agree.visualisation import BiDisagreements
>>>
>>> agreements = pd.DataFrame({"olly": [0, 1, None, 3], "rob": [0, 1, 1, 3], "cal": [0, 1, 2, 3]})
>>> labels = [0, 1, 2, 3]
>>>
>>> bidis = BiDisagreements(agreements, labels)
>>> bidis.agreements_summary()
Number of instances with:
=========================
No disagreement: 3
Bidisagreement: 1
Tridisagreement: 0
More disagreements: 0
>>>
>>> bidisagreement_matrix = bidis.agree_matrix()
>>> bidis.visualise(title="Example matrix")
>>> print(bidisagreement_matrix)
[[0. 0. 0. 0.]
 [0. 0. 1. 0.]
 [0. 1. 0. 0.]
 [0. 0. 0. 0.]]

"""
import numpy as np
import pandas as pd
import sys
import math
import itertools
import matplotlib.pyplot as plt


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
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Data input must be a pandas DataFrame")

        for type_ in df.dtypes:
            if not (type_ == int or type_ == float):
                raise TypeError("DataFrame entries must be int types, float types, or NaN")

        if not isinstance(labels, list):
            raise TypeError("Argument 2 must be of type list.")

        if not all(isinstance(n, int) for n in labels):
            raise TypeError("All elements in list of labels must be of type int")

        self.df = df
        self.labels = labels
        n = len(self.labels)
        self.agreements_matrix = np.zeros((n, n))
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
                self.agreements_matrix[key1][key2] = dict_[key1][key2]

    def agree_matrix(self):
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

        return self.agreements_matrix

    def visualise(self, cmap="Reds", normalise=True, title=""):
        """
        Displays the bidisagreement matrix as a plot

        Parameters
        ----------
        cmap: string, optional (default "Reds")
            See matplotlib.pylab.pyplot.get_cmap for possible values
            Will throw an internal ValueError if invalid input.
        normalise: boolean, optional (default True)
            If True, normalises disagreement quantities by horizontal row
            If False, gives absolute disagreement quantities
        title: string, optional (default "")
            Title for the visualisation
        """
        cm = self.agreements_matrix
        cmap = plt.get_cmap(cmap)

        plt.imshow(cm, interpolation="nearest", cmap=cmap)
        plt.title(title, fontsize=10)
        plt.colorbar()

        tick_marks = np.arange(len(self.labels))
        plt.xticks(tick_marks, self.labels, rotation=45)
        plt.yticks(tick_marks, self.labels)

        if normalise:
            if cm.sum(axis=None) > 0.:
                numerator = cm.astype("float")
                denom = cm.sum(axis=1)
                cm = np.divide(numerator, denom, out=np.zeros_like(numerator), where=denom!=0)
            else:
                cm = cm.astype("float")

        thresh = cm.max() / 1.5 if normalise else cm.max() / 2
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if normalise:
                s = "{:0.2f}"
            else:
                s = "{:,}"
            plt.text(j, i, s.format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black",
                     fontsize=8)

        plt.tight_layout(pad=0.00001)
        plt.ylabel("Label")
        plt.xlabel("Label")
        plt.show()


if __name__ == "__main__":
    test_annotations_1 = {"a": [None, None, None, None, None, 1, 3, 0, 1, 0, 0, 2, 2, None, 2],
                          "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
                          "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}
    df1 = pd.DataFrame(test_annotations_1)
    labels = [0, 1, 2, 3]
    instance1 = BiDisagreements(df1, labels)
    instance1.agreements_summary()