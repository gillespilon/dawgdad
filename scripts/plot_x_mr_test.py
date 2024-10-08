#! /usr/bin/env python3
"""
Test X and mR of control_charts.py

time -f "%e" ./control_charts.py
./control_charts.py
"""

import time

from dawgdad.import control_charts as cc
import matplotlib.pyplot as plt
import dawgdad as dd
import pandas as pd

graph_mr_file_name = "plot_mr_test.svg"
graph_x_file_name = "plot_x_test.svg"
output_url = "plot_x_mr_test.html"
header_title = "plot_x_mr_test"
header_id = "plot-x-mr-test"
figsize = (8, 6)


def main():
    start_time = time.time()
    original_stdout = dd.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    data = dd.random_data(
        distribution="norm",
        size=42,
        loc=69,
        scale=13
    )
    data = pd.DataFrame(
        data=data,
        columns=["X"]
    )
    # Create X control chart
    dd.page_break()
    fig = plt.figure(figsize=figsize)
    x = cc.X(data=data)
    ax = x.ax(fig=fig)
    fig.savefig(fname=graph_x_file_name)
    dd.html_figure(file_name=graph_x_file_name)
    print(
       f"X Report\n"
       f"============\n"
       f"UCL        : {x.ucl.round(3)}\n"
       f"Xbar       : {x.mean.round(3)}\n"
       f"LCL        : {x.lcl.round(3)}\n"
       f"Sigma(X)   : {x.sigma.round(3)}\n"
    )
    # Create mr chart
    fig = plt.figure(figsize=figsize)
    mr = cc.mR(data=data)
    ax = mr.ax(fig=fig)
    fig.savefig(fname=graph_mr_file_name)
    dd.html_figure(file_name=graph_mr_file_name)
    print(
       f"mR Report\n"
       f"============\n"
       f"UCL        : {mr.ucl.round(3)}\n"
       f"mRbar      : {mr.mean.round(3)}\n"
       f"LCL        : {round(mr.lcl, 3)}\n"
       f"Sigma(mR)  : {mr.sigma.round(3)}\n"
    )
    stop_time = time.time()
    dd.page_break()
    dd.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    dd.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == "__main__":
    main()
