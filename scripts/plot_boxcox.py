#! /usr/bin/env python3
"""
Example of boxcox plot.
"""

from pathlib import Path

from scipy import stats
import dawgdad as dd


def main():
    dd.style_graph()
    s = stats.loggamma.rvs(5, size=500) + 5
    fig, ax = dd.plot_boxcox(s=s)
    ax.set_title(label='Box-Cox plot')
    fig.savefig(fname=Path('box_cox_plot.svg'))


if __name__ == '__main__':
    main()
