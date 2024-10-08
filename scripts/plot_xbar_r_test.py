#! /usr/bin/env python3
"""
Test Xbar and R of control_charts.py

time -f "%e" ./control_charts.py
./control_charts.py
"""

import time

from dawgdad.import control_charts as cc
import matplotlib.pyplot as plt
import dawgdad as dd
import pandas as pd

graph_xbar_file_name = "plot_xbar_test.svg"
graph_r_file_name = "plot_r_test.svg"
output_url = "plot_xbar_r_test.html"
header_title = "plot_xbar_r_test"
header_id = "plot-xbar-r-test"
figsize = (8, 6)


def main():
    start_time = time.time()
    original_stdout = dd.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    X1 = dd.random_data(
        distribution="norm",
        size=25,
        loc=69,
        scale=13
    )
    X2 = dd.random_data(
        distribution="norm",
        size=25,
        loc=69,
        scale=13
    )
    X3 = dd.random_data(
        distribution="norm",
        size=25,
        loc=69,
        scale=13
    )
    X4 = dd.random_data(
        distribution="norm",
        size=25,
        loc=69,
        scale=13
    )
    data = pd.DataFrame(
        data={
            "X1": X1,
            "X2": X2,
            "X3": X3,
            "X4": X4,
        }
    )
    # Create Xbar control chart
    dd.page_break()
    fig = plt.figure(figsize=figsize)
    xbar = cc.Xbar(data=data)
    ax = xbar.ax(fig=fig)
    fig.savefig(fname=graph_xbar_file_name)
    dd.html_figure(file_name=graph_xbar_file_name)
    print(
       f"Xbar Report\n"
       f"============\n"
       f"UCL        : {xbar.ucl.round(3)}\n"
       f"Xbarbar    : {xbar.mean.round(3)}\n"
       f"LCL        : {xbar.lcl.round(3)}\n"
       f"Sigma(Xbar): {xbar.sigma.round(3)}\n"
    )
    # Create R chart
    fig = plt.figure(figsize=figsize)
    r = cc.R(data=data)
    ax = r.ax(fig=fig)
    fig.savefig(fname=graph_r_file_name)
    dd.html_figure(file_name=graph_r_file_name)
    print(
       f"R Report\n"
       f"============\n"
       f"UCL        : {r.ucl.round(3)}\n"
       f"Rbar       : {r.mean.round(3)}\n"
       f"LCL        : {round(r.lcl, 3)}\n"
       f"Sigma(R)   : {r.sigma.round(3)}\n"
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
