import logging
import unittest
import sys

import pandas as pd

sys.path.append("..")

from metrics import Krippendorff

test_annotations = {"a": [None, None, None, None, None, 2, 3, 0, 1, 0, 0, 2, 2, None, 2],
                    "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
                    "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}
labels = [0, 1, 2, 3]
df = pd.DataFrame(test_annotations)

kripp = Krippendorff(df, labels)


class TestKrippendorff(unittest.TestCase):
    """
    Tests for Krippendorff's alpha computations from
    disagree.metrics.Krippendorff
    """
    def final_alpha_value_with_nominal_data(self):
        # Test the final value of kripps alpha, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
        alpha = kripp.alpha(data_type="nominal")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.691)

    def final_alpha_value_with_interval_data(self):
        # Test the final value of kripps alpha, from the Wikipedia example
        # https://en.wikipedia.org/wiki/Krippendorff%27s_alpha
        alpha = kripp.alpha(data_type="interval")
        alpha = float("{:.3f}".format(alpha))
        self.assertTrue(alpha == 0.811)


if __name__ == "__main__":
    unittest.main()
