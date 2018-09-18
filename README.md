# disagree - Assessing Annotator Disagreements in Python

This library aims to address annotation disagreements in manually labelled data.

## Install

To install, setup a virtualenv and do:

`$ python3 -m pip install --index-url https://pypi.org/project/ disagree`

## Background

Whilst working in NLP, I've been repeatedly working with datasets that have been manually labelled, and have thus had to evaluate the quality of the agreements between the annotators. In my (limited) experience of doing this, I have encountered a number of ways of it that have been helpful. In this library, I aim to group all of those things together for people to use.

Please suggest any additions if you have any.

## Summary of features

* Visualisations
  * Ability to visualise bidisagreements between annotators
  * Ability to visualise agreement statistics
  * Retrieve summaries of numbers of disagreements and their extent

* Annotation statistics:
  * Joint probability
  * Cohens kappa
  * Fleiss kappa
  * Pearson, Spearman, Kendall correlations
  * Krippendorff's alpha

## Python examples

Partial examples can be found at the top of the source code. Worked examples are also provided in the Jupyter notebooks.

## Documentation

### **disagree.agreements.BiDisagreements(df, labels)**

`BiDisagreements` class is primarily there for you to visualise the disagreements in the form of a matrix, but has some other small functionalities.

There are some quite strict requirements with regards to the parameters here. (See usage example in notebooks or top of source code.)

* `df`: Pandas DataFrame containing annotator labels
  * ***Rows***: Instances of the data that is labelled
  * ***Columns***: Annotators
  * Element [i, j] is annotator j's label for data instance i.
  * Entries must be integers, floats, or pandas nan values
  * The lowest label must be 0. E.g. if your labels are 1-5, convert them to 0-4.

* `labels`: list containing possible labels
  * Must be from 0 to the maximum label. If your labels are words then please convert them to corresponding integers.
  * Example: If the labels are [male, female, trans], you must convert to [0, 1, 2]

* **Attributes**:
  * **`agreements_summary()`**
    * This will print out statistics on the number of instances with no disagreements, the number of bidisagreements, the number of tridisagreements, and the number of instances with worse cases (i.e. 3+ disagreements).
  * **`agreements_matrix()`**
    * This will return a matrix of bidisagreements. Do with this what you will!
    * Element [i, j] is the number of times there is a bidisagreement involving label i and label j.
  * **`visualise(cmap="Reds", normalise=True, title="Bidisagreements")`**
    * Used to visualise the agreements_matrix described above.
    * Parameter: cmap, string, optional -- The cmaps colour you would like in the matrix visualisation (see matplotlib for possible values)
    * Parameter: normalise, boolean, optional -- If True, normalise the disagreement counts. If False, present absolute disagreement counts
    * Parameter: title, string, optional -- Title for the disagreements matrix

### **disagree.metrics.Metrics(df, labels)**

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

  * **`correlation(ann1, ann2, measure="pearson")`**
    * Parameter: ann1, string, name of one of the annotators from the DataFrame columns
    * Parameter: ann2, string, name of one of the annotators from the DataFrame columns
    * Paramater: measure, string, optional
      * Options: (pearson (default), kendall, spearman)
    * This gives you either pearson , kendall, or spearman correlation statistics between two annotators

  * **visualise_metric(func, cmap="Blues", title="")**
    * Returns a matrix of size (num_annotators x num_annotators). Element [i, j] is the statistic value for agreements between annotator i and annotator j.
    * Parameter: func, name of function for the metric you want to visualise.
      * Options: (metrics.Metrics.cohens_kappa, metrics.Metrics.joint_probability)
    * Parameter: cmap, string, optional -- The cmaps colour you would like in the matrix visualisation (see matplotlib for possible values)
    * Parameter: title, string, optional -- Title for the disagreements matrix

### **disagree.metrics.Krippendorff(df, labels)**

See above for df and labels args.

* **Attributes**
  * **`alpha(data_type="nominal")`**
    * In this library, Krippendorff's alpha can handle four data types, one of which must be specified:
      * nominal (default)
      * ordinal
      * interval
      * ratio
