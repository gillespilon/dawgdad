"""
Shewhart control charts

Create X, mR, Xbar, R control charts
Invoke Shewhart rules 1, 2, 3, 4
"""

from typing import Iterable, TypeVar
from collections import defaultdict
from abc import ABC, abstractmethod
from itertools import tee
from math import sqrt

from cached_property import cached_property
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import pandas as pd
import numpy as np


colour1 = '#0077bb'
colour2 = '#33bbee'
colour3 = '#009988'
colour4 = '#cc3311'

CONSTANTS: pd.DataFrame = pd.DataFrame.from_dict(
    dict(
        n=np.array([
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 100]),
        A2=np.array([
            1.881, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308,
            0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203, 0.194, 0.187,
            0.180, 0.173, 0.167, 0.162, 0.157, 0.153, 0.134, 0.120, 0.110,
            0.101, 0.094, 0.088, 0.083, 0.079, 0.075, 0.072, 0.069, 0.066,
            0.064, 0.060]),
        A3=np.array([
            2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975,
            0.927, 0.886, 0.850, 0.817, 0.789, 0.763, 0.739, 0.718, 0.698,
            0.680, 0.663, 0.647, 0.633, 0.619, 0.606]),
        B3=np.array([
            0, 0, 0, 0, 0.030, 0.118, 0.185, 0.239, 0.284, 0.321, 0.354,
            0.382, 0.406, 0.428, 0.448, 0.466, 0.482, 0.497, 0.510, 0.523,
            0.534, 0.545, 0.555, 0.565]),
        B4=np.array([
            3.267, 2.568, 2.266, 2.089, 1.970, 1.882, 1.815, 1.761, 1.716,
            1.679, 1.646, 1.618, 1.594, 1.572, 1.552, 1.534, 1.518, 1.503,
            1.490, 1.477, 1.466, 1.455, 1.445, 1.435]),
        c2=np.array([
            0.5642, 0.7236, 0.7979, 0.8407, 0.8686, 0.8882, 0.9027, 0.9139,
            0.9227, 0.9300, 0.9359, 0.9410, 0.9453, 0.9490, 0.9523, 0.9551,
            0.9576, 0.9599, 0.9619, 0.9638, 0.9655, 0.9670, 0.9684, 0.9695,
            0.9748, 0.9784, 0.9811, 0.9832, 0.9849, 0.9863, 0.9874, 0.9884,
            0.9892, 0.9900, 0.9906, 0.9911, 0.9916, 0.9925]),
        c4=np.array([
            0.7979, 0.8862, 0.9213, 0.9400, 0.9515, 0.9594, 0.9650, 0.9693,
            0.9727, 0.9754, 0.9776, 0.9794, 0.9810, 0.9823, 0.9835, 0.9845,
            0.9854, 0.9862, 0.9869, 0.9876, 0.9882, 0.9887, 0.9892, 0.9896]),
        d2=np.array([
            1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078,
            3.173, 3.258, 3.336, 3.407, 3.472, 3.532, 3.588, 3.640, 3.689,
            3.735, 3.778, 3.819, 3.858, 3.895, 3.931, 4.086, 4.213, 4.322,
            4.415, 4.498, 4.572, 4.639, 4.699, 4.755, 4.806, 4.854, 4.898,
            4.939, 5.015]),
        d3=np.array([
            0.8525, 0.8884, 0.8798, 0.8641, 0.8480, 0.8332, 0.8198, 0.8078,
            0.7971, 0.7873, 0.7785, 0.7704, 0.7630, 0.7562, 0.7499, 0.7441,
            0.7386, 0.7335, 0.7287, 0.7272, 0.7199, 0.7159, 0.7121, 0.7084,
            0.6927, 0.6799, 0.6692, 0.6601, 0.6521, 0.6452, 0.6389, 0.6333,
            0.6283, 0.6236, 0.6194, 0.6154, 0.6118, 0.6052]),
        D3=np.array([
            'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 0.076, 0.136, 0.184, 0.223,
            0.256, 0.283, 0.307, 0.328, 0.347, 0.363, 0.378, 0.391, 0.403,
            0.415, 0.423, 0.434, 0.443, 0.452, 0.459, 0.491, 0.516, 0.535,
            0.551, 0.565, 0.577, 0.587, 0.596, 0.604, 0.611, 0.617, 0.623,
            0.628, 0.638]),
        d4=np.array([
            0.954, 1.588, 1.978, 2.257, 2.472, 2.645, 2.791, 2.915, 3.024,
            3.121, 3.207, 3.285, 3.356, 3.422, 3.482, 3.538, 3.591, 3.640,
            3.686, 3.730, 3.771, 3.811, 3.847, 3.883, 4.037, 4.166, 4.274,
            4.372, 4.450, 4.521, 4.591, 4.649, 4.707, 4.757, 4.806, 4.849,
            4.892, 4.968]),
        D4=np.array([
            3.267, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816, 1.777,
            1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622, 1.609, 1.597,
            1.585, 1.577, 1.566, 1.557, 1.548, 1.541, 1.509, 1.484, 1.465,
            1.449, 1.435, 1.423, 1.413, 1.404, 1.396, 1.389, 1.383, 1.377,
            1.372, 1.362]),
        E2=np.array([
            2.660, 1.772, 1.457, 1.290, 1.184, 1.109, 1.054, 1.010, 0.975,
            0.945, 0.921, 0.899, 0.881, 0.864, 0.849, 0.836, 0.824, 0.813,
            0.803, 0.794, 0.786, 0.778, 0.770, 0.763, 0.734, 0.712, 0.694,
            0.680, 0.667, 0.656, 0.647, 0.638, 0.631, 0.624, 0.618, 0.612,
            0.607, 0.598])
    ),
    orient='index').transpose().set_index('n')


def _despine(ax: axes.Axes) -> None:
    """
    Remove the top and right spines of a graph.

    There is only one x axis, on the bottom, and one y axis, on the left.

    Parameters
    ----------
    ax : axes.Axes
        The Axes on which to act.
    """
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


class Sigmas:
    def __init__(self, mean: float, sigma: float):
        self._mean = mean
        self._sigma = sigma

    def __getitem__(self, index: int | slice) -> float:
        if isinstance(index, int):
            return self._mean + index * self._sigma
        elif isinstance(index, slice):
            raise NotImplementedError()
        else:
            raise ValueError()


class ControlChart(ABC):
    def __init__(self, data: pd.DataFrame):
        self._df = data

    @cached_property
    @abstractmethod
    def ucl(self) -> float:  # pragma: no cover
        """
        Calculate the upper control limit
        """
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def lcl(self) -> float:  # pragma: no cover
        """
        Calculate the lower control limit
        """
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def sigma(self) -> float:  # pragma: no cover
        """
        Calculate the standard deviation appropriate to method used
        """
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def mean(self) -> float:  # pragma: no cover
        """
        Calculate the average
        """
        raise NotImplementedError()

    @cached_property
    @abstractmethod
    def y(self) -> pd.Series:  # pragma: no cover
        """
        The y coordinates of the points on a plot of this chart
        """
        raise NotImplementedError()

    @abstractmethod
    def ax(self,
           fig: plt.Figure = None) -> axes.Axes:  # pragma: no cover
        'Matplotlib control chart plot'
        raise NotImplementedError()

    # @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    @cached_property
    def sigmas(self):
        """
        TODO

        Ex:

            cc = ControlChart(some_data)
            cc.x - cc.mean * 3 == .X_chart.sigmas[-3]
        """
        return Sigmas(mean=self.mean, sigma=self.sigma)

    # TODO: cache
    def _average_mr(self, subgroup_size: int = 2) -> float:
        """
        Calculate the average moving range
        """
        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        _ = self._df.iloc[:, 0]
        return (
            _.rolling(subgroup_size).max() -
            _.rolling(subgroup_size).min()
        ).mean()


class X(ControlChart):
    """
    Individual values control chart (X)
    """
    def __init__(self, data: pd.DataFrame, subgroup_size: int = 2):
        super().__init__(data)

        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        self.subgroup_size = subgroup_size

    @cached_property
    def _d2(self) -> float:
        return CONSTANTS['d2'].loc[self.subgroup_size]

    @cached_property
    def sigma(self) -> float:
        """
        Sigma(X)

        Standard deviation using rational subgroup estimator
        """
        return self._average_mr(self.subgroup_size) / self._d2

    @cached_property
    def ucl(self) -> float:
        """
        Upper control limit
        """
        return self.mean + 3 * self.sigma

    @cached_property
    def lcl(self) -> float:
        """
        Lower control limit
        """
        return self.mean - 3 * self.sigma

    @cached_property
    def mean(self) -> float:
        """
        Average(X)
        """
        return self._df.iloc[:, 0].mean()

    @cached_property
    def y(self) -> pd.Series:
        return self._df[self._df.columns[0]]

    def ax(self, fig: plt.Figure = None) -> axes.Axes:
        """
        Plots individual values of the column of the dataframe (y axis) versus
        the index of the dataframe (x axis)

        Parameters
        ----------
        fig: plt.Figure = None
            A matplotlib figure.

        Returns
        -------
        axes: Axes
            A matplotlib Axes.

        Examples
        --------
        minimal X control chart

        >>> import dawgdad.control_charts as cc
        >>> import matplotlib.pyplot as plt
        >>> import dawgdad as dd
        >>> import pandas as pd
        >>> figsize = (8, 6)
        >>> graph_name = 'graph_x.svg'
        >>> data = dd.random_data(
        ...     distribution='norm',
        ...     size=42,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data=data,
        ...     columns=['X']
        ... )
        >>> fig = plt.figure(figsize=figsize)
        >>> x = cc.X(data=data)
        >>> ax = x.ax(fig=fig)
        >>> plt.tight_layout()
        >>> fig.savefig(fname=graph_name)

        complete X control chart

        >>> figsize = (8, 6)
        >>> graph_name = 'graph_x.svg'
        >>> colour='#33bbee'
        >>> data = dd.random_data(
        ...     distribution='norm',
        ...     size=42,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data=data,
        ...     columns=['X']
        ... )
        >>> fig = plt.figure(figsize=figsize)
        >>> x = cc.X(data=data)
        >>> ax = x.ax(fig=fig)
        >>> ax.axhline(
        ...     y=x.sigmas[+1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=x.sigmas[-1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=x.sigmas[+2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=x.sigmas[-2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> cc.draw_rules(x, ax)
        >>> ax.set_title(
        ...     label="X chart title",
        ...     fontweight="bold"
        ... ) # doctest: +SKIP
        >>> ax.set_ylabel(ylabel="X chart Y label") # doctest: +SKIP
        >>> ax.set_xlabel(xlabel="X chart X label") # doctest: +SKIP
        >>> fig.savefig(fname=graph_name)
        """
        if fig is None:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        _despine(ax)
        ax.plot(self.y.index, self.y,
                marker='o', markersize=3, color=colour1)
        ax.axhline(
            y=self.mean,
            color=colour3
        )
        ax.axhline(
            y=self.ucl,
            color=colour1
        )
        ax.axhline(
            y=self.lcl,
            color=colour1
        )

        return ax


class mR(ControlChart):
    """
    Moving range of individual values control chart (mR)
    """
    def __init__(self, data: pd.DataFrame, subgroup_size: int = 2):
        super().__init__(data)

        if subgroup_size is None:
            subgroup_size = 2
        assert subgroup_size >= 2
        self.subgroup_size = subgroup_size

    @cached_property
    def _d2(self) -> float:
        return CONSTANTS['d2'].loc[self.subgroup_size]

    @cached_property
    def _d3(self) -> float:
        return CONSTANTS['d3'].loc[self.subgroup_size]

    @cached_property
    def sigma(self) -> float:
        """
        Sigma(mR)

        Standard deviation using rational subgroup estimator
        """
        return self._average_mr(self.subgroup_size) * self._d3 / self._d2

    @cached_property
    def ucl(self) -> float:
        """
        Upper control limit
        """
        return self._average_mr(self.subgroup_size) + 3 * self.sigma

    @cached_property
    def lcl(self) -> float:
        """
        Lower control limit
        """
        r_chart_lcl = self._average_mr(self.subgroup_size) - 3 * self.sigma
        if r_chart_lcl < 0:
            r_chart_lcl = 0
        return r_chart_lcl

    @cached_property
    def mean(self) -> float:
        """
        Average(mR)
        """
        return self._average_mr(self.subgroup_size)

    @cached_property
    def y(self) -> pd.Series:
        df = (
            self._df.rolling(self.subgroup_size).max() -
            self._df.rolling(self.subgroup_size).min()
        )
        return df[df.columns[0]]

    def ax(self, fig: plt.Figure = None) -> axes.Axes:
        """
        Plots calculated moving ranges (y axis) versus
        the index of the dataframe (x axis)

        Parameters
        ----------
        fig: plt.Figure = None
            A matplotlib figure.

        Returns
        -------
        axes: Axes
            A matplotlib Axes.

        Examples
        --------
        minimal mR control chart

        >>> import dawgdad.control_charts as cc
        >>> import matplotlib.pyplot as plt
        >>> import dawgdad as dd
        >>> import pandas as pd
        >>> figsize = (8, 6)
        >>> graph_name = 'graph_mr.svg'
        >>> data = dd.random_data(
        ...     distribution='norm',
        ...     size=42,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data=data,
        ...     columns=['X']
        ... )
        >>> fig = plt.figure(figsize=figsize)
        >>> mr = cc.mR(data=data)
        >>> ax = mr.ax(fig=fig)
        >>> fig.savefig(fname=graph_name)

        complete mR control chart

        >>> figsize = (8, 6)
        >>> graph_name = 'graph_mr.svg'
        >>> data = dd.random_data(
        ...     distribution='norm',
        ...     size=42,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data=data,
        ...     columns=['X']
        ... )
        >>> mr = cc.mR(data=data)
        >>> ax = mr.ax(fig=fig)
        >>> cc.draw_rule(mr, ax, *cc.points_one(mr), '1')
        >>> ax.set_title(
        ...     label="mR chart title",
        ...     fontweight="bold"
        ... ) # doctest: +SKIP
        >>> ax.set_ylabel(ylabel="mR chart Y label") # doctest: +SKIP
        >>> ax.set_xlabel(xlabel="mR chart X label") # doctest: +SKIP
        >>> fig.savefig(fname=graph_name)
        """
        if fig is None:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        _despine(ax)
        ax.plot(self.y.index, self.y,
                marker='o', markersize=3, color=colour2)
        # TODO? ax.set_xlim(0, len(self._df.columns))
        ax.axhline(
            y=self.mean,
            color=colour3
        )
        ax.axhline(
            y=self.ucl,
            color=colour1
        )
        ax.axhline(
            y=self.lcl,
            color=colour1
        )

        return ax


class Xbar(ControlChart):
    """
    Average of a subgroup of values control chart (Xbar)
    """
    @cached_property
    def _average_range(self) -> float:
        'Calculate the average range'
        return (
            self._df.max(axis='columns') -
            self._df.min(axis='columns')
        ).mean()

    @cached_property
    def _subgroup_size(self) -> int:
        return len(self._df.columns)

    @cached_property
    def _d2(self) -> float:
        return CONSTANTS['d2'].loc[len(self._df.columns)]

    @cached_property
    def mean(self) -> float:
        """
        Average(Xbar)
        """
        return self._df.mean(axis='columns').mean()

    @cached_property
    def ucl(self) -> float:
        """
        Upper control limit
        """
        return (
            self.mean
            + 3
            * self._average_range
            / (self._d2 * sqrt(self._subgroup_size))
        )

    @cached_property
    def lcl(self) -> float:
        """
        Lower control limit
        """
        return (
            self.mean
            - 3
            * self._average_range
            / (self._d2 * sqrt(self._subgroup_size))
        )

    @cached_property
    def y(self) -> pd.Series:
        return self._df.mean(axis='columns')

    def ax(self, fig: plt.Figure = None) -> axes.Axes:
        """
        Plots calculated averages (y axis) versus
        the index of the dataframe (x axis)

        Parameters
        ----------
        fig: plt.Figure = None
            A matplotlib figure.

        Returns
        -------
        axes: Axes
            A matplotlib Axes.

        Examples
        --------
        minimal Xbar control chart

        >>> import dawgdad.control_charts as cc
        >>> import matplotlib.pyplot as plt
        >>> import dawgdad as dd
        >>> import pandas as pd
        >>> figsize = (8, 6)
        >>> graph_name = 'graph_xbar.svg'
        >>> colour='#33bbee'
        >>> X1 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X2 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X3 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X4 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data={
        ...         'X1': X1,
        ...         'X2': X2,
        ...         'X3': X3,
        ...         'X4': X4,
        ...     }
        ... )
        >>> fig = plt.figure(figsize=figsize)
        >>> xbar = cc.Xbar(data=data)
        >>> ax = xbar.ax(fig=fig)
        >>> fig.savefig(fname=graph_name)

        complete Xbar control chart

        >>> figsize = (8, 6)
        >>> graph_name = 'graph_xbar.svg'
        >>> colour='#33bbee'
        >>> X1 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X2 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X3 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X4 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data={
        ...         'X1': X1,
        ...         'X2': X2,
        ...         'X3': X3,
        ...         'X4': X4,
        ...     }
        ... )
        >>> fig = plt.figure(figsize=figsize)
        >>> xbar = cc.Xbar(data=data)
        >>> ax = xbar.ax(fig=fig)
        >>> ax.axhline(
        ...     y=xbar.sigmas[+1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=xbar.sigmas[-1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=xbar.sigmas[+2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=xbar.sigmas[-2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> cc.draw_rules(xbar, ax) # doctest: +SKIP
        >>> ax.set_title(
        ...     label="Xbar chart title",
        ...     fontweight="bold"
        ... ) # doctest: +SKIP
        >>> ax.set_ylabel(ylabel="Xbar chart Y label") # doctest: +SKIP
        >>> ax.set_xlabel(xlabel="Xbar chart X label") # doctest: +SKIP
        >>> fig.savefig(fname=graph_name)
        """
        if fig is None:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        _despine(ax)
        ax.plot(self.y.index, self.y,
                marker='o', markersize=3, color=colour2)
        ax.axhline(
            y=self.mean,
            color=colour3
        )
        ax.axhline(
            y=self.ucl,
            color=colour1
        )
        ax.axhline(
            y=self.lcl,
            color=colour1
        )
        return ax

    @cached_property
    def sigma(self) -> float:
        """
        Sigma(Xbar)

        Standard deviation using rational subgroup estimator
        """
        return self._average_range / self._d2 / sqrt(self._subgroup_size)


class R(ControlChart):
    """
    Range of a subgroup of values control chart (R)
    """
    @cached_property
    def _d2(self) -> float:
        return CONSTANTS['d2'].loc[len(self._df.columns)]

    @cached_property
    def _d3(self) -> float:
        return CONSTANTS['d3'].loc[len(self._df.columns)]

    @cached_property
    def mean(self) -> float:
        """
        Average(R)
        """
        return (
            self._df.max(axis='columns') - self._df.min(axis='columns')
        ).mean()

    @cached_property
    def ucl(self) -> float:
        """
        Upper control limit
        """
        return (
            self.mean
            + 3
            * self._d3
            * self.mean
            / self._d2
        )

    @cached_property
    def lcl(self) -> float:
        """
        Lower control limit
        """
        ret = (
            self.mean
            - 3
            * self._d3
            * self.mean
            / self._d2
        )
        # Set the moving range lower control limit to 0 if it is < 0.
        if ret < 0:
            ret = 0.0
        return ret

    @cached_property
    def y(self) -> pd.Series:
        return (
            self._df.max(axis='columns')
            - self._df.min(axis='columns')
        )

    def ax(self, fig: plt.Figure = None) -> axes.Axes:
        """
        Plots calculated ranges (y axis) versus
        the index of the dataframe (x axis)

        Parameters
        ----------
        fig: plt.Figure = None
            A matplotlib figure.

        Returns
        -------
        axes: Axes
            A matplotlib Axes.

        Examples
        --------
        minimal R control chart

        >>> import dawgdad.control_charts as cc
        >>> import matplotlib.pyplot as plt
        >>> import dawgdad as dd
        >>> import pandas as pd
        >>> figsize = (8, 6)
        >>> graph_name = 'graph_r.svg'
        >>> X1 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X2 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X3 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X4 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data={
        ...         'X1': X1,
        ...         'X2': X2,
        ...         'X3': X3,
        ...         'X4': X4,
        ...     }
        ... )
        >>> graph_r_file_name = 'graph_r.svg'
        >>> fig = plt.figure(figsize=(8, 6))
        >>> r = cc.R(data=data)
        >>> ax = r.ax(fig=fig)
        >>> fig.savefig(fname=graph_r_file_name)

        complete R control chart

        >>> figsize = (8, 6)
        >>> graph_name = 'graph_r.svg'
        >>> colour='#33bbee'
        >>> X1 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X2 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X3 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> X4 = dd.random_data(
        ...     distribution='norm',
        ...     size=25,
        ...     loc=69,
        ...     scale=13,
        ...     random_state=42
        ... )
        >>> data = pd.DataFrame(
        ...     data={
        ...         'X1': X1,
        ...         'X2': X2,
        ...         'X3': X3,
        ...         'X4': X4,
        ...     }
        ... )
        >>> fig = plt.figure(figsize=(8, 6))
        >>> r = cc.R(data=data)
        >>> ax = r.ax(fig=fig)
        >>> ax.axhline(
        ...     y=r.sigmas[+1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=r.sigmas[-1],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=r.sigmas[+2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> ax.axhline(
        ...     y=r.sigmas[-2],
        ...     linestyle='--',
        ...     dashes=(5, 5),
        ...     color=colour,
        ...     alpha=0.5
        ... ) # doctest: +SKIP
        >>> cc.draw_rule(r, ax, *cc.points_one(r), '1')
        >>> ax.set_title(
        ...     label="R chart",
        ...     fontweight="bold"
        ... ) # doctest: +SKIP
        >>> ax.set_ylabel(ylabel="Y label") # doctest: +SKIP
        >>> ax.set_xlabel(xlabel="X label") # doctest: +SKIP
        >>> graph_r_file_name = 'graph_r.svg'
        >>> fig.savefig(fname=graph_r_file_name)
        """
        if fig is None:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        _despine(ax)
        ax.plot(self.y.index, self.y,
                marker='o', markersize=3, color=colour2)
        ax.axhline(
            y=self.mean,
            color=colour3
        )
        ax.axhline(
            y=self.ucl,
            color=colour1
        )
        ax.axhline(
            y=self.lcl,
            color=colour1
        )
        return ax

    @cached_property
    def sigma(self) -> float:
        """
        Sigma(R)

        Standard deviation using rational subgroup estimator
        """
        return self.mean * self._d3 / self._d2


def draw_rule(
    cc: ControlChart,
    ax: axes.Axes,
    above: pd.Series,
    below: pd.Series,
    rule_name: str
) -> None:
    """
    Invokes one of the points_* rules to identify out-of-control points

    Parameters
    ----------
    cc : ControlChart
        The control chart object.
    ax : axes.Axes
        The Axes object.
    above : pd.Series
        The pandas Series for the points above rule.
    below : pd.Series
        The pandas Series for the points below a rule.
    """
    y_percent = (cc.y.max() - cc.y.min()) / 100

    for x, y in above.items():
        ax.annotate(rule_name, xy=(x, y), xytext=(x, y + y_percent * 5),
                    color=colour4)

    for x, y in below.items():
        ax.annotate(rule_name, xy=(x, y), xytext=(x, y - y_percent * 5),
                    color=colour4)


# We can't use for group in series.rolling(5) because it's not implemened yet,
# since 2015. We also can't use rolling(3) (on a bool column) .sum() >= 2
# because we wouldn't know whether to annotate point 2 or 3 in a group. At that
# point, you'd have to write manual Python code to figure it out. Just do a
# plain old Python loop.
# Here's the rolling code until we realised it wouldn't work.
#    cc.y.loc[(cc.y > cc.sigmas[2]).rolling(2).sum() >= 2]


# TODO: Split into separate finder and plotter.
def draw_rules(cc: ControlChart, ax: axes.Axes) -> None:
    """
    Invokes all of the points_* rules to identify out-of-control points

    Parameters
    ----------
    cc : ControlChart
        The control chart object.
    ax : axes.Axes
        The Axes object.
    """
    aboves = defaultdict(str)
    belows = defaultdict(str)
    for label, rule in [('1', points_one),
                        ('2', points_two),
                        ('3', points_three),
                        ('4', points_four)]:
        above, below = rule(cc)
        for x, y in above.items():
            aboves[(x, y)] += label
        for x, y in below.items():
            belows[(x, y)] += label

    y_percent = (cc.y.max() - cc.y.min()) / 100

    for (x, y), rule_names in aboves.items():
        ax.annotate(rule_names, xy=(x, y), xytext=(x, y + y_percent * 5),
                    color=colour4)

    for (x, y), rule_names in belows.items():
        ax.annotate(rule_names, xy=(x, y), xytext=(x, y - y_percent * 5),
                    color=colour4)


T = TypeVar('T')


def _nwise(it: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    """
    Creates iterable m of n for points rules
    """
    its = tee(it, n)
    for it_i in range(1, n):
        for tee_times in range(it_i):
            next(its[it_i], None)
    return zip(*its)


def points_one(cc: ControlChart) -> tuple[pd.Series, pd.Series]:
    """
    Return out of control points as Series of only said points

    Shewhart and Western Electric Rule one.
    Nelson and Minitab rule one.
    One point outside the three-sigma limits.
    This rule is used with the X, mR, Xbar, and R charts.

    Parameters
    ----------
    cc : ControlChart
        The control chart object.

    Returns
    -------
    tuple[pd.Series]
        A tuple containing two elements, the data points that are out of
        control for rule one.

        - series_above: pd.Series
            The series of points above the control limit.
        - series_below: pd.Series
            The series of points below the control limit.
    """
    points_above = cc.y[cc.y > cc.ucl]
    points_below = cc.y[cc.y < cc.lcl]
    return (points_above, points_below)


def points_two(cc: ControlChart) -> tuple[pd.Series, pd.Series]:
    """
    Return out of control points as Series of only said points

    Shewhart and Western Electric rule two.
    Nelson and Minitab rule five.
    Two-out-of-three successive points on the same side of the central line
    and both are more than two sigma units away from the central line.
    This rule is used with the X and Xbar charts.

    Parameters
    ----------
    cc : ControlChart
        The control chart object.

    Returns
    -------
    tuple[pd.Series]
        A tuple containing two elements, the data points that are out of
        control for rule two.

        - series_above: pd.Series
            The series of points above the control limit.
        - series_below: pd.Series
            The series of points below the control limit.
    """

    points_above = []
    points_below = []
    for group in _nwise(cc.y.items(), 3):
        above_in_window = [(x, y)
                           for x, y
                           in group
                           if y > cc.sigmas[+2]]
        if len(above_in_window) >= 2:
            points_above.append(above_in_window[1])  # whether 2 or 3, 2nd
        below_in_window = [(x, y)
                           for x, y
                           in group
                           if y < cc.sigmas[-2]]
        if len(below_in_window) >= 2:
            points_below.append(below_in_window[1])  # whether 2 or 3, 2nd
    series_above = (pd.Series(dict(points_above), dtype='float64'))
    series_below = (pd.Series(dict(points_below), dtype='float64'))
    return (series_above, series_below)


def points_three(cc: ControlChart) -> tuple[pd.Series, pd.Series]:
    """
    Return out of control points as Series of only said points

    Shewhart or Western Electric rule three.
    Nelson or Minitab rule six.
    Four-out-of-five successive points on the same side of the central line
    and are more than one sigma units away from the central line.
    This rule is used with the X and Xbar charts.

    Parameters
    ----------
    cc : ControlChart
        The control chart object.

    Returns
    -------
    tuple[pd.Series]
        A tuple containing two elements, the data points that are out of
        control for rule three.

        - series_above: pd.Series
            The series of points above the control limit.
        - series_below: pd.Series
            The series of points below the control limit.
    """
    points_above = []
    points_below = []
    for group in _nwise(cc.y.items(), 5):
        above_in_window = [(x, y)
                           for x, y
                           in group
                           if y > cc.sigmas[+1]]
        if len(above_in_window) >= 4:
            points_above.append(above_in_window[3])  # whether 4 or 5, 4th point
        below_in_window = [(x, y)
                           for x, y
                           in group
                           if y < cc.sigmas[-1]]
        if len(below_in_window) >= 4:
            points_below.append(below_in_window[3])  # whether 4 or 5, 4th point
    series_above = (pd.Series(dict(points_above), dtype='float64'))
    series_below = (pd.Series(dict(points_below), dtype='float64'))
    return (series_above, series_below)


def points_four(cc: ControlChart) -> tuple[pd.Series, pd.Series]:
    """
    Return out of control points as Series of only said points

    Shewhart and Western Electric rule four.
    Nelson and Minitab rule two.
    Eight successive points all on the same side of the central line.
    This rule is used with the X and Xbar charts.

    Parameters
    ----------
    cc : ControlChart
        The control chart object.

    Returns
    -------
    tuple[pd.Series]
        A tuple containing two elements, the data points that are out of
        control for rule four.

        - series_above: pd.Series
            The series of points above the control limit.
        - series_below: pd.Series
            The series of points below the control limit.
    """
    count_above = 0
    count_below = 0
    points_above = []
    points_below = []
    for x, y in cc.y.items():
        if y > cc.mean:
            count_above += 1
            count_below = 0
        elif y < cc.mean:
            count_above = 0
            count_below += 1
        if count_above >= 8:
            points_above.append((x, y))
        elif count_below >= 8:
            points_below.append((x, y))
    series_above = (pd.Series(dict(points_above), dtype='float64'))
    series_below = (pd.Series(dict(points_below), dtype='float64'))
    return (series_above, series_below)


__all__ = (
    'ControlChart',
    'points_three',
    'points_four',
    'points_two',
    'points_one',
    'draw_rules',
    'draw_rule',
    'Xbar',
    'mR',
    'R',
    'X',
)
