import logging
import unittest
import sys

import pandas as pd

sys.path.append("..")
from metrics import Krippendorff
from metrics import Metrics

test_annotations = {"a": [None, None, None, None, None, 2, 3, 0, 1, 0, 0, 2, 2, None, 2],
                    "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
                    "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}
df = pd.DataFrame(test_annotations)

kripp = Krippendorff(df)
mets = Metrics(df)


class TestMetrics(unittest.TestCase):
    """
    Tests for Krippendorff's alpha computations from
    disagree.metrics.Krippendorff
    """
    def test_kripps_alpha_value_with_nominal_data(self):
        # Test the final value of kripps alpha, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
        alpha = kripp.alpha(data_type="nominal")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.691)

    def test_kripps_alpha_value_with_interval_data(self):
        # Test the final value of kripps alpha, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
        alpha = kripp.alpha(data_type="interval")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.811)

    def test_joint_probability_value(self):
        jp = mets.joint_probability(ann1="a", ann2="b")
        actual_jp = 2 / 3
        self.assertTrue(jp == actual_jp)

    def test_cohens_kappa_value(self):
        pass

    def test_df2table_function(self):
        pass

    def test_proportion_label_per_category_function(self):
        pass

    def test_rater_agreement_extent_function(self):
        pass

    def test_fleiss_kappa_value(self):
        pass

    def test_correlation_function(self):
        pass

    def test_metric_matrix_function(self):
        pass

    def test_instance_degree_function(self):
        pass

    def test_bidisagreement_degree_function(self):
        pass


if __name__ == "__main__":
    unittest.main()
