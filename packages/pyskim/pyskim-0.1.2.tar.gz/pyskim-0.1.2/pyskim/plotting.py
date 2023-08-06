import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


def annotate_correlation(*args, method, **kwargs):
    """Plot correlation.

    Adapted from https://github.com/mwaskom/seaborn/issues/1444
    """
    # TODO: handle hue

    # compute correlation
    corr_r = args[0].corr(args[1], method)
    corr_text = f'{corr_r:2.2f}'.replace('0.', '.')

    # visualize correlation
    ax = plt.gca()
    ax.set_axis_off()

    marker_size = abs(corr_r) * 10000
    ax.scatter(
        .5, .5, marker_size, corr_r, alpha=0.6,
        cmap='vlag_r', vmin=-1, vmax=1,  # bwr_r
        transform=ax.transAxes
    )

    ax.annotate(
        corr_text,
        [.5, .5], xycoords='axes fraction',
        ha='center', va='center', fontsize=20
    )

    return ax


def corrplot(
    df: pd.DataFrame,
    corr_method: str = 'spearman', **kwargs
) -> sns.PairGrid:
    """An improved version of `sns.pairplot`."""
    g = sns.PairGrid(df, **kwargs)

    g.map_upper(annotate_correlation, method=corr_method)
    g.map_diag(sns.distplot, kde=False)
    g.map_lower(sns.scatterplot, rasterized=True)  # regplot

    return g
