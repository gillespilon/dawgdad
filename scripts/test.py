#! /usr/bin/env python3
import matplotlib.pyplot as plt
import dawgdad as dd
X = dd.random_data(distribution='uniform').sort_values()
y = dd.random_data(distribution='norm')
p = dd.natural_cubic_spline(
    X=X,
    y=y,
    number_knots=10
)
fig, ax = dd.plot_scatter_line_x_y1_y2(
    X=X,
    y1=y,
    y2=p.predict(X)
)
plt.show()
