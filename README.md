# annotations

This library aims to address annotation disagreements in manually labelled data.

## Install

To install, do: ...

## Background

Whilst working in NLP, I've been repeatedly working with datasets that have been manually labelled, and have thus had to evaluate the quality of the agreements between the annotators. In my (limited) experience of doing this, I have encountered a number of ways of it that have been helpful. In this library, I aim to group all of those things together for people to use.

## Summary of features

* Visualisations
  * Ability to visualise bidisagreements between annotators
  * Retrieve summaries of number of cases with no disagreements, bidisagreements, tridisagreements, and more

* Annotation statistics:
  * Joint probability
  * Cohens kappa
  * Fleiss kappa
  * Pearson, Spearman, Kendall correlations
  * Krippendorff's alpha

## Python examples

These examples can be found at the top of the respective source codes as well.

The first example demonstrates agree visualisations:

```
from annotations.visualisation import BiDisagreements
from annotations.metrics import Metrics, Krippendorff
import pandas as pd

agreements = pd.DataFrame({"olly": [0, 1, None, 3], "rob": [0, 1, 1, 3], "cal": [0, 1, 2, 3]})
labels = [0, 1, 2, 3]

bidis = BiDisagreements(agreements, labels)
bidis.agreements_summary()
# This would show a summary of agreements

bidisagreement_matrix = bidis.agree_matrix()
bidis.visualise(title="Example matrix")
print(bidisagreement_matrix)

[[0. 0. 0. 0.]
 [0. 0. 1. 0.]
 [0. 1. 0. 0.]
 [0. 0. 0. 0.]]
```

This second example demonstrates the use of statistical metrics for assessing agreements:

```

anns = {"a": [None, None, None, None, None, 2, 3, 0, 1, 0, 0, 2, 2, None, 2],
        "b": [0, None, 1, 0, 2, 2, 3, 2, None, None, None, None, None, None, None],
        "c": [None, None, 1, 0, 2, 3, 3, None, 1, 0, 0, 2, 2, None, 3]}

df = pd.DataFrame(anns)
labels = [0, 1, 2, 3]

mets = Metrics(df, labels)
kripp = Krippendorff(df, labels)

ann1 = "a"
ann2 = "b"

joint_prob = joint_probability(ann1, ann2)
cohens_kappa = mets.cohens_kappa(ann1, ann2)
fleiss_kappa = mets.fleiss_kappa()
pearson_corr = mets.correlation(ann1, ann2, "pearson")
kendall_corr = mets.correlation(ann1, ann2, "kendall")
spearman_corr = mets.correlation(ann1, ann2, "spearman")
kripps_alpha = kripp.alpha(data_type="nominal")
```

## Documentation

### **annotations.visualisation.BiDisagreements(df, labels)**

BiDisagreements are primarily there for you to visualise the disagreements in the form of a matix.

There are some quite strict requirements with regards to the parameters here. (See usage example in notebooks or top of source code.)

* `df`: Pandas DataFrame containing annotator labels
  * ***Rows***: Instances of the data that is labelled
  * ***Columns***: Annotators
  * Element [i, j] is annotator j's label for data instance i.
  * Entries must be integers, floats, or pandas nan values

* `labels`: list containing possible labels
  * Must be from 0 to the maximum label. If your labels are words then please convert them to corresponding integers.
  * Example: If the labels are [male, female, trans], you must convert to [0, 1, 2]

* **Attributes**:
  * **`agreements_summary()`**
    * This will print out statistics on the number of instances with no disagreements, the number of bidisagreements, the number of tridisagreements, and the number of instances with worse cases (i.e. 4+ disagreements).
  * **`agree_matrix()`**
    * This will return a matrix of bidisagreements. Do with this what you will!
  * **`visualise(cmap, normalise, title)`**
    * Parameter: cmap, string -- The cmaps colour you would like in the matrix visualisation (see matplotlib)
    * Parameter: normalise, boolean -- If True, normalise the disagreement counts. If False, present absolute disagreement counts
    * Parameter: title, string -- Title for the disagreements matrix

### **annotations.metrics.Metrics(df, labels)**

This module gives you access to a number of metrics typically used for annotation disagreement statistics.

See above for df and labels args.

* **Attributes**:
  * **`joint_probability(ann1, ann2)`**
    * Parameter: ann1, string, name of one of the annotators from the DataFrame columns
    * Parameter: ann2, string, name of one of the annotators from the DataFrame columns
    * This gives the join probability of agreement between ann1 and ann2. You should probably not use this measure for academic purposes, but is here for completion.

  * **`cohens_kappa(ann1, ann2)`**:
    * Parameter: ann1, string, name of one of the annotators from the DataFrame columns
    * Parameter: ann2, string, name of one of the annotators from the DataFrame columns

  * **`fliess_kappa()`**
    * No args

  * **`correlation(ann1, ann2, measure)`**
    * Parameter: ann1, string, name of one of the annotators from the DataFrame columns
    * Parameter: ann2, string, name of one of the annotators from the DataFrame columns
    * Paramater: measure, string
      * Options: (pearson, kendall, spearman)
    * This gives you either pearson , kendall, or spearman correlation statistics between two annotators

### **agree.metrics.Krippendorff(df, labels)**

See above for df and labels args.

* **Attributes**
  * **`alpha(data_type)`**
    * In this library, Krippendorff's alphs can handle four data types, one of which must be specified:
      * Nominal (assumed)
      * Ordinal
      * Interval
      * Ratio
