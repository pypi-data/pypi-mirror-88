from typing import List, Optional

from pandas import DataFrame
from examplecurves import make_family_overview_plots

import examplecurves
import matplotlib.pyplot as plt


def plot_curves_dev(curves: List[DataFrame], title: Optional[str]=None):
    """
    Plots curves within a diagram.

    Args:
        curves(List[DataFrame]):
            Curves to plot.

        title(Optional[str]):
            Optional title for the diagram.

    """
    fig = plt.figure(figsize=(8, 5), dpi=96, tight_layout=True)
    gs = fig.add_gridspec(1, 10)
    axes = fig.add_subplot(gs[:, :9])
    if title:
        axes.set_title(title)
    for index, curve in enumerate(curves):
        axes.plot(curve, "-o", label=str(index))
    fig.legend(loc="upper right", bbox_to_anchor=(0.99, 0.945))
    fig.show()

examplecurves.plot_curves = plot_curves_dev

make_family_overview_plots("nonlinear0")
