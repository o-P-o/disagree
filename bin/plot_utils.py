import matplotlib.pyplot as plt
import numpy as np
import itertools


def matrix_plot(cm, labels, cmap, title):
    cmap = plt.get_cmap(cmap)

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title, fontsize=10)
    plt.colorbar()

    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)

    thresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        s = "{:,}"
        plt.text(j, i, s.format(cm[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",
                 fontsize=8)

    plt.tight_layout(pad=0.00001)
    plt.ylabel("Annotator")
    plt.xlabel("Annotator")
    plt.show()
