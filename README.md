# disagree - Assessing Annotator Disagreements in Python

This library aims to address annotation disagreements in manually labelled data.

I started it as a project to develop some understanding of Python packaging and workflow. (This is
the primary reason for the messy release history and commit logs, for which I apologise.) But I hope this will be useful for a wider audience as well.

## Install

To install, setup a virtualenv and do:

`$ python3 -m pip install --index-url https://pypi.org/project/ disagree`

or

`$ pip3 install disagree`

To update to the latest version do:

`$ pip3 install --upgrade disagree`

## Background

Whilst working in NLP, I've been repeatedly working with datasets that have been manually labelled, and have thus had to evaluate the quality of the agreements between the annotators. In my (limited) experience of doing this, I have encountered a number of ways of it that have been helpful. In this library, I aim to group all of those things together for people to use.

Please suggest any additions/functionalities, and I will try my best to add them.

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

Worked examples are provided in the Jupyter notebooks directory.

## Documentation

### **disagree.BiDisagreements(df)**

`BiDisagreements` class is primarily there for you to visualise the disagreements in the form of a matrix, but has some other small functionalities.

* `df`: Pandas DataFrame containing annotator labels
  * ***Rows***: Instances of the data that is labelled
  * ***Columns***: Annotators
  * Element [i, j] is annotator j's label for data instance i.
  * Entries must be integers, floats, strings, or pandas nan values

* **Attributes**:
  * **`agreements_summary()`**
    * This will print out statistics on the number of instances with no disagreements, the number of bidisagreements, the number of tridisagreements, and the number of instances with worse cases (i.e. 3+ disagreements).
  * **`agreements_matrix()`**
    * This will return a matrix of bidisagreements. Do with this what you will! The intention is that
    you use something like matplotlib to visualise them properly.
    * Element $(i, j)$ is the number of times there is a bidisagreement involving label $i$ and label $j$.
  * **`labels_to_index()`**
    * Returns a dictionary mapping label names to indexes used in the `agreements_matrix()`.

### **disagree.metrics.Metrics(df)**

This module gives you access to a number of metrics typically used for annotation disagreement statistics.

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

  * **metric_matrix(func)**
    * Returns a matrix of size (num_annotators x num_annotators). Element $(i, j)$ is the statistic value for agreements between annotator $i$ and annotator $j$.
    * Parameter: func, name of function for the metric you want to visualise.
      * Options: (metrics.Metrics.cohens_kappa, metrics.Metrics.joint_probability)

### **disagree.metrics.Krippendorff(df)**

* **Attributes**
  * **`alpha(data_type="nominal")`**
    * In this library, Krippendorff's alpha can handle four data types, one of which must be specified:
      * nominal (default)
      * ordinal
      * interval
      * ratio
