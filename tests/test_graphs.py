import dawgdad as dd


def test_plot_scatterleft_scatterright_x_y1_y2():
    pass


def test_plot_scatter_scatter_x1_x2_y1_y2():
    pass


def test_plot_lineleft_lineright_x_y1_y2():
    pass


def test_plot_barleft_lineright_x_y1_y2():
    pass


def test_plot_line_line_line_x_y1_y2_y3():
    pass


def test_plot_scatter_scatter_x_y1_y2():
    pass


def test_plot_scatter_line_x_y1_y2():
    pass


def test_plot_line_line_x_y1_y2():
    pass


def test_plot_horizontal_bars():
    pass


def test_plot_line_line_y1_y2():
    pass


def test_plot_vertical_bars():
    pass


def test_plot_stacked_bars():
    pass


def test_probability_plot():
    pass


def test_plot_scatter_x_y():
    pass


def test_plot_histogram():
    pass


def test_plot_scatter_y():
    pass


def test_plot_line_x_y():
    pass


def test_format_dates():
    pass


def test_plot_boxplot():
    pass


def test_plot_line_y():
    pass


def test_plot_pareto():
    pass


def test_style_graph():
    pass


def test_dd_to_dms():
    decdeg = [45.4250225, -75.6970594]
    result = dd.dd_to_dms(decdeg=decdeg)
    expected = [(45, 25, 30.081, 'N'), (75, 41, 49.41384, 'W')]
    assert result == expected
    decdeg = [48.858393, 2.257616]
    result = dd.dd_to_dms(decdeg=decdeg)
    expected = [(48, 51, 30.2148, 'N'), (2, 15, 27.4176, 'E')]
    assert result == expected
    decdeg = [-13.163194, -72.547842]
    result = dd.dd_to_dms(decdeg=decdeg)
    expected = [(13, 9, 47.4984, 'S'), (72, 32, 52.2312, 'W')]
    assert result == expected
    decdeg = [-33.8567433, 151.1784306]
    result = dd.dd_to_dms(decdeg=decdeg)
    expected = [(33, 51, 24.27588, 'S'), (151, 10, 42.35016, 'E')]
    assert result == expected

def test_dms_to_dd():
    dms = [(45, 25, 30.081, 'N'), (75, 41, 49.41384, 'W')]
    result = dd.dms_to_dd(dms=dms)
    expected = [45.4250225, -75.6970594]
    assert result == expected
    dms = [(48, 51, 30.2148, 'N'), (2, 15, 27.4176, 'E')]
    result = dd.dms_to_dd(dms=dms)
    expected = [48.858393, 2.257616]
    assert result == expected
    dms = [(13, 9, 47.4984, 'S'), (72, 32, 52.2312, 'W')]
    result = dd.dms_to_dd(dms=dms)
    expected = [-13.163194, -72.547842]
    assert result == expected
    dms = [(33, 51, 24.27588, 'S'), (151, 10, 42.35016, 'E')]
    result = dd.dms_to_dd(dms=dms)
    expected = [-33.8567433, 151.1784306]
    assert result == expected


def test_plot_pie():
    pass


def test_despine():
    pass


def test_qr_code():
    pass
