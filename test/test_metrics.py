import sys
import unittest
import pandas as pd

sys.path.append("..")
from metrics import Krippendorff
from metrics import Metrics

test_annotations = {"a": [None, None, None, None, None, 2, 3, 0, 1, 0, 0, 2, 2, None, 2],
                    "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
                    "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}

data_binary = {"a": [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
               "b": [1, 1, 1, 0, 0, 1, 0, 0, 0, 0]}

data_nominal_full = {"a": ['a', 'a', 'b', 'b', 'd', 'c', 'c', 'c', 'e', 'd', 'd', 'a'],
                     "b": ['b', 'a', 'b', 'b', 'b', 'c', 'c', 'c', 'e', 'd', 'd', 'd']}

data_nominal_missing = {"a": [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
                        "b": [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
                        "c": [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
                        "d": [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None]}

data_cohens = {"a": [1 for _ in range(20)] + [0 for _ in range(15)] + [1 for _ in range(5)] + [0 for _ in range(10)],
               "b": [1 for _ in range(20)] + [0 for _ in range(15)] + [0 for _ in range(5)] + [1 for _ in range(10)]}

data_fleiss = {"1": [5, 2, 3, 2, 1, 1, 1, 1, 1, 2],
               "2": [5, 2, 3, 2, 1, 1, 1, 1, 1, 2],
               "3": [5, 3, 3, 2, 2, 1, 1, 2, 1, 3],
               "4": [5, 3, 4, 3, 2, 1, 2, 2, 1, 3],
               "5": [5, 3, 4, 3, 3, 1, 2, 2, 1, 4],
               "6": [5, 3, 4, 3, 3, 1, 3, 2, 1, 4],
               "7": [5, 3, 4, 3, 3, 1, 3, 2, 2, 4],
               "8": [5, 3, 4, 3, 3, 2, 3, 3, 2, 5],
               "9": [5, 4, 5, 3, 3, 2, 3, 3, 2, 5],
               "10": [5, 4, 5, 3, 3, 2, 3, 3, 2, 5],
               "11": [5, 4, 5, 3, 3, 2, 3, 4, 2, 5],
               "12": [5, 4, 5, 3, 3, 2, 4, 4, 3, 5],
               "13": [5, 5, 5, 4, 4, 2, 4, 5, 3, 5],
               "14": [5, 5, 5, 4, 5, 2, 4, 5, 4, 5],
               }

df_test = pd.DataFrame(test_annotations)
df_binary = pd.DataFrame(data_binary)
df_nominal_full = pd.DataFrame(data_nominal_full)
df_nominal_missing = pd.DataFrame(data_nominal_missing)
df_cohens = pd.DataFrame(data_cohens)
df_fleiss = pd.DataFrame(data_fleiss)

kripp_binary = Krippendorff(df_binary)
kripp_nominal_full = Krippendorff(df_nominal_full)
kripp_nominal_missing = Krippendorff(df_nominal_missing)

kripp_test = Krippendorff(df_test)
kripp_binary = Krippendorff(df_binary)
kripp_nominal_full = Krippendorff(df_nominal_full)
kripp_nominal_missing = Krippendorff(df_nominal_missing)

mets = Metrics(df_test)
mets_cohens = Metrics(df_cohens)
mets_fleiss = Metrics(df_fleiss)


class TestMetrics(unittest.TestCase):
    """
    Tests for Krippendorff's alpha computations from
    disagree.metrics.Krippendorff
    """
    def test_kripps_alpha_value_with_binary_data(self):
        # Test the final value of kripps alpha, from Krippendorff paper
        # Page 3
        alpha = kripp_binary.alpha(data_type="nominal")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.095)

    def test_kripps_alpha_value_with_nominal_full_data(self):
        # Test the final value of kripps alpha, from Krippendorff paper
        # Page 4
        alpha = kripp_nominal_full.alpha(data_type="nominal")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.692)

    def test_kripps_alpha_value_with_nominal_missing_data(self):
        # Test the final value of kripps alpha, from Krippendorff paper
        # Page 5
        alpha = kripp_nominal_missing.alpha(data_type="nominal")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.743)

    def test_kripps_alpha_value_with_interval_data(self):
        # Test the final value of kripps alpha, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
        alpha = kripp_test.alpha(data_type="interval")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.811)

    def test_joint_probability_value(self):
        jp = mets.joint_probability(ann1="a", ann2="b")
        actual_jp = 2 / 3
        self.assertTrue(jp == actual_jp)

    def test_cohens_kappa_value(self):
        # Test the final value of Cohen's kappa, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Cohen%27s_kappa
        cohens = mets_cohens.cohens_kappa(ann1="a", ann2="b")
        cohens = float("{:.3f}".format(cohens))
        self.assertTrue(cohens == 0.400)

    def test_fleiss_kappa_value(self):
        # Test the final value of Fleiss' kappa, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Fleiss%27_kappa
        fleiss = mets_fleiss.fleiss_kappa()
        fleiss = float("{:.3f}".format(fleiss))
        self.assertTrue(fleiss == 0.210)


if __name__ == "__main__":
    unittest.main()
