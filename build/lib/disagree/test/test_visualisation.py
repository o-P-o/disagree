import logging
import unittest
import sys

import pandas as pd

sys.path.append("..")
import agreements

test_annotations = {"a": [None, None, None, None, None, 1, 3, 0, 1, 0, 0, 2, 2, None, 2],
                    "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
                    "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}
df = pd.DataFrame(test_annotations)
labels = [0, 1, 2, 3]
instance = agreements.BiDisagreements(df, labels)


class TestBiDisagreements(unittest.TestCase):
    """
    Tests for visualisation.py, with the aim of testing unit in the
    agree.visualisation.BiDisagreements class
    """
    def test_full_agreement_count(self):
        count = instance.agreements_summary()[0]
        self.assertTrue(count == 9)

    def test_bi_disagreement_count(self):
        count = instance.agreements_summary()[1]
        self.assertTrue(count == 2)

    def test_tri_disagreement_count(self):
        count = instance.agreements_summary()[2]
        self.assertTrue(count == 1)

    def test_more_disagreement_count(self):
        count = instance.agreements_summary()[3]
        self.assertTrue(count == 0)

    def test_agreements_matrix(self):
        mat = instance.agreements_matrix()
        self.assertTrue(mat[0][2] == 1. and mat[2][0] == 1. and mat[2][3] == 1. and mat[3][2] == 1.)


if __name__ == "__main__":
    unittest.main()
