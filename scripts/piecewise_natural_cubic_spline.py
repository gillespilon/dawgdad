#! /usr/bin/env python3
"""
A piecewise natural cubic spline (cubic curves in the interior segments, linear
in the exterior segments) is used to interpolate points to fit the data while
smoothing out the noise. A large number of data are fitted with low-degree
polynomials, to eliminate excessive oscillations and non-convergence.

References

[Drury, Matthew. Basis Expansions](https://github.com/madrury/basis-expansions)

[Leal, Lois Anne. Numerical Interpolation: Natural Cubic Spline]
(https://towardd.atascience.com/numerical-interpolation-natural-cubic-spline
-52c1157b98ac)

[SAS/GRAPH SYMBOL Statement (INTERPOL=SM&lt;nn&gt;&lt;P&gt;&lt;S&gt;)]
(https://documentation.sas.com/?docsetId=graphref&docsetTarget=n0c0j84n1e2jz9n
1bhkn41o3v0d6.htm&docsetVersion=9.4&locale=en#p115cutvcmx2dln1cdo96duwmxru)

[Wikipedia. Smoothing spline](https://en.wikipedia.org/wiki/Smoothing_spline)

[Wikipedia. Spline (mathematics)]
(https://en.wikipedia.org/wiki/Spline_(mathematics))

time -f '%e' ./piecewise_natural_cubic_spline.py
./piecewise_natural_cubic_spline.py

The graphs can be viewed with the view_spline_graphs.html file created.
"""

from multiprocessing import Pool
from typing import List, NoReturn, Tuple
import time

import dawgdad as dd
import pandas as pd


def main():
    start_time = time.time()
    global figsize, axis_title, x_axis_label, y_axis_label,\
        graphics_directory
    file_names, targets, features, number_knots, graphics_directory,\
        figsize, x_axis_label, y_axis_label, axis_title,\
        date_parser, output_url, header_title, header_id = parameters()
    dd.create_directory(directories=graphics_directory)
    original_stdout = dd.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    dd.page_break()
    for file_name, target, feature in zip(file_names, targets, features):
        data = dd.read_file(
            file_name=file_name,
            parse_dates=features
        )
        data[target] = data[target].fillna(data[target].mean())
        dates = True
        X = pd.to_numeric(data[feature])
        y = data[target]
        t = ((X, y, file_name, target, feature, knot, dates)
             for knot in number_knots)
        with Pool() as pool:
            for _ in pool.imap_unordered(plot_scatter_line, t):
                pass
        for knot in number_knots:
            dd.html_figure(
                file_name=f'{graphics_directory}/'
                          f'spline_{file_name.strip(".csv")}_'
                          f'{target}_{feature}_{knot}.svg'
            )
    stop_time = time.time()
    dd.page_break()
    dd.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        read_file_names=file_names,
        targets=targets,
        features=features,
        number_knots=number_knots
    )
    dd.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def parameters(
) -> (
    List[str],
    List[str],
    List[str],
    List[int],
    str,
    Tuple[int, int],
    str,
    str,
    str,
    str,
    str,
    str,
    str
):
    """
    Set parameters.
    """

    parameters = dd.read_file(
        file_name='piecewise_natural_cubic_spline_parameters.odd.
    )
    file_names = [x for x in parameters['File names'] if str(x) != 'nan']
    targets = [x for x in parameters['Targets'] if str(x) != 'nan']
    features = [x for x in parameters['Features'] if str(x) != 'nan']
    number_knots = [int(x) for x in parameters['Number of knots']
                    if str(x) != 'nan']
    datetimeparser = parameters['Other parameter values'][0]
    graphicsdirectory = parameters['Other parameter values'][1]
    figurewidthheight = eval(parameters['Other parameter values'][2])
    xaxislabel = parameters['Other parameter values'][3]
    yaxislabel = parameters['Other parameter values'][4]
    axistitle = parameters['Other parameter values'][5]
    output_url = parameters['Other parameter values'][6]
    header_title = parameters['Other parameter values'][7]
    header_id = parameters['Other parameter values'][8]
    return (
        file_names, targets, features, number_knots, graphicsdirectory,
        figurewidthheight, xaxislabel, yaxislabel, axistitle,
        datetimeparser, output_url, header_title, header_id
    )


def plot_scatter_line(
        t: Tuple[pd.Series, pd.Series, int, int, str, str, str, int, bool]
) -> NoReturn:
    X, y, file_name, target, feature, number_knots, dates = t
    model = dd.natural_cubic_spline(
        X=X,
        y=y,
        number_knots=number_knots
    )
    if dates:
        XX = X.astype(dtype='datetime64[ns]')
    else:
        XX = X
    fig, ax = dd.plot_scatter_line_x_y1_y2(
        X=XX,
        y1=y,
        y2=model.predict(X),
        figsize=figsize,
        labellegendy2=f'number knots = {number_knots}'
    )
    ax.legend(frameon=False, loc='best')
    ax.set_title(
        label=f'{axis_title}\n'
              f'file: {file_name} '
              f'column: {target}'
    )
    ax.set_xlabel(xlabel=x_axis_label)
    ax.set_ylabel(ylabel=y_axis_label)
    dd.despine(ax=ax)
    fig.savefig(
        f'{graphics_directory}'
        f'/spline_'
        f'{file_name.strip(".csv")}_'
        f'{target}_{feature}_'
        f'{number_knots}.svg',
        format='svg'
    )


if __name__ == '__main__':
    main()
