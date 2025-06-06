from pytest import approx, mark
import warnings

import dawgdad as dd
import pandas as pd
import numpy as np


warnings.filterwarnings("ignore")
X = pd.Series(
    data=[
        25.0, 24.0, 35.5, 22.4, 23.1, 13.9, 13.9, 10.0, 13.3, 10.0, 16.0,
        16.0, 16.0
    ]
)
df_integer_float = pd.DataFrame(
    data={
        "abscissa": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "ordinate": [
            0,
            0.841470984807896,
            0.909297426825682,
            0.141120008059867,
            -0.756802495307928,
            -0.958924274663138,
            -0.279415498198926,
            0.656986598718789,
            0.989358246623382,
            0.412118485241757,
        ],
    }
)
df_datetime_float = pd.DataFrame(
    data={
        "abscissa": [
            "2020-01-01 12:00:00",
            "2020-01-02 12:00:00",
            "2020-01-03 12:00:00",
            "2020-01-04 12:00:00",
            "2020-01-05 12:00:00",
            "2020-01-06 12:00:00",
            "2020-01-07 12:00:00",
            "2020-01-08 12:00:00",
            "2020-01-09 12:00:00",
            "2020-01-10 12:00:00",
        ],
        "ordinate": [
            0,
            0.841470984807896,
            0.909297426825682,
            0.141120008059867,
            -0.756802495307928,
            -0.958924274663138,
            -0.279415498198926,
            0.656986598718789,
            0.989358246623382,
            0.412118485241757,
        ],
    }
).astype(dtype={"abscissa": "datetime64[s]"})
series1_two_sample_t = pd.Series(
    data=[32, 37, 35, 28, 41, 44, 35, 31, 34, 38, 42], name="y1"
)
series2_two_sample_t = pd.Series(
    data=[36, 31, 30, 31, 34, 36, 29, 32, 31],
    name="y2"
)
series_one_sample_t = pd.Series(
    data=[
        211,
        572,
        558,
        250,
        478,
        307,
        184,
        435,
        460,
        308,
        188,
        111,
        676,
        326,
        142,
        255,
        205,
        77,
        190,
        320,
        407,
        333,
        488,
        374,
        409,
    ]
)
df_linear_regression = pd.DataFrame(
    data={
        "X": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
        "y": [
            8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68
        ],
    }
)
series1_paired = pd.Series(
    data=[
        68,
        76,
        74,
        71,
        71,
        72,
        75,
        83,
        75,
        74,
        76,
        77,
        78,
        75,
        75,
        84,
        77,
        69,
        75,
        65,
    ],
    name="before",
)
series2_paired = pd.Series(
    data=[
        67,
        77,
        74,
        74,
        69,
        70,
        71,
        77,
        71,
        74,
        73,
        68,
        71,
        72,
        77,
        80,
        74,
        73,
        72,
        62,
    ],
    name="after",
)


def test_nonparametric_summary():
    """
    Test for method 8
    """
    result = dd.nonparametric_summary(
        series=X, alphap=1/3, betap=1/3, decimals=3
    )
    expected = pd.Series(
        data={
            "lower outer fence": -15.4,
            "lower inner fence": -0.85,
            "lower quartile": 13.7,
            "median": 16.0,
            "confidence interval": (11.776, 20.224),
            "upper quartile": 23.4,
            "upper inner fence": 37.95,
            "upper outer fence": 52.5,
            "interquartile range": 9.7,
            "inner outliers": [],
            "outer outliers": [],
            "minimum value": 10.0,
            "maximum value": 35.5,
            "count": 13,
        }
    )
    assert result.equals(other=expected)


def test_parametric_summary():
    result = dd.parametric_summary(series=X, decimals=3)
    expected = pd.Series(
        data={
            "n": 13,
            "min": 10.0,
            "max": 35.5,
            "ave": 18.392,
            "confidence interval": (14.013, 22.772),
            "s": 7.248,
            "var": 52.527,
        }
    )
    assert result.equals(other=expected)


@mark.parametrize(
    "df, expected",
    [
        (
            df_integer_float,
            (
                0.0,
                0.841470984807896,
                0.909297426825682,
                0.141120008059867,
                -0.756802495307928,
                -0.958924274663138,
                -0.279415498198926,
                0.656986598718789,
                0.989358246623382,
                0.41211848524175704,
            ),
        ),
        (
            df_datetime_float,
            (
                0.0,
                0.841470984807896,
                0.909297426825682,
                0.141120008059867,
                -0.756802495307928,
                -0.958924274663138,
                -0.279415498198926,
                0.656986598718789,
                0.989358246623382,
                0.41211848524175704,
            ),
        ),
    ],
)
def test_cubic_spline(df, expected):
    cubic_spline = dd.cubic_spline(
        df=df,
        abscissa="abscissa",
        ordinate="ordinate"
    )
    result = tuple(cubic_spline(x=df["abscissa"]))
    assert result == expected


@mark.parametrize(
    "df, n_knots, random_seed, expected_predictions",
    [
        (
            df_linear_regression,
            10,
            41,
            np.array(
                [
                    -8.449636,
                    -7.369397,
                    -6.950373,
                    -10.332163,
                    -6.039679,
                    -10.662885,
                    -8.113000,
                    -5.399096,
                    -11.197986,
                    -10.397764,
                    -9.309493,
                    -10.481590,
                    -9.887573,
                ]
            ),
        ),
        # You can add more test cases here with different data,
        # number of knots, random seeds, and expected predictions.
        # For example:
        # (
        #     pd.DataFrame({"X": [1, 2, 3], "y": [2, 4, 6]}),
        #     2,
        #     42,
        #     np.array([1.9999999, 4.0000000, 6.0000000]) # Example expected values
        # ),
    ],
)
def test_natural_cubic_spline(df, n_knots, random_seed, expected_predictions):
    pipeline_fit = dd.natural_cubic_spline(
        X=df["X"],
        y=df["y"],
        number_knots=n_knots
    )
    X = dd.random_data(size=len(expected_predictions), random_state=random_seed).values
    predictions = pipeline_fit.predict(X=X)
    result = pd.Series(data=predictions)
    expected = pd.Series(data=expected_predictions)
    assert np.allclose(result, expected, atol=1e-5)


@mark.parametrize(
    "size, random_state, expected_data",
    [
        (
            13,
            41,
            [
                -0.2707123230673205,
                0.10484805260974006,
                0.25052781572357197,
                -0.9251999652780767,
                0.567143660285906,
                -1.040180216082938,
                -0.15367595145793744,
                0.7898518103468191,
                -1.2262158464418542,
                -0.9480069877134585,
                -0.5696539419300647,
                -0.9771502146977724,
                -0.7706317111835508,
            ],
        ),
        (
            5,
            100,
            [
                -1.7497654730546974,
                0.34268040332750216,
                1.153035802563644,
                -0.25243603652138985,
                0.9813207869512316
            ]
        ),
        # Add more test cases here by varying size and random_state
        # and providing the corresponding expected data.
        # >>> import dawgdad as dd
        # >>> import pandas as pd
        # >>> import numpy as np
        # >>>
        # >>> size = 5
        # >>> random_state = 100
        # >>> generated_data = dd.random_data(size=size, random_state=random_state)
        # >>> print(generated_data.tolist())
    ],
)
def test_random_data(size, random_state, expected_data):
    result = dd.random_data(size=size, random_state=random_state)
    expected = pd.Series(data=expected_data)
    assert result.equals(other=expected)


# def test_datetime_data():
#     result = dd.datetime_data(
#         start_year="2020",
#         start_month="01",
#         start_day="01",
#         start_hour="00",
#         start_minute="00",
#         start_second="00",
#         end_year="2020",
#         end_month="01",
#         end_day="01",
#         end_hour="07",
#         end_minute="00",
#         end_second="00",
#         time_delta_days=7,
#         time_delta_hours=1,
#     )
#     expected = pd.Series(
#         data=[
#             "2020-01-01 00:00:00",
#             "2020-01-01 01:00:00",
#             "2020-01-01 02:00:00",
#             "2020-01-01 04:00:00",
#             "2020-01-01 03:00:00",
#             "2020-01-01 05:00:00",
#             "2020-01-01 06:00:00",
#         ]
#     ).astype(dtype="datetime64[s]")
#     assert result.equals(other=expected)


@mark.parametrize(
    "start_year, start_month, start_day, start_hour, start_minute, "
    " start_second, end_year, end_month, end_day, end_hour, end_minute, "
    "end_second, time_delta_days, time_delta_hours, expected_data",
    [
        (
            "2020", "01", "01", "00", "00", "00",
            "2020", "01", "01", "07", "00", "00",
            7, 1,
            [
                "2020-01-01 00:00:00",
                "2020-01-01 01:00:00",
                "2020-01-01 02:00:00",
                "2020-01-01 03:00:00",
                "2020-01-01 04:00:00",
                "2020-01-01 05:00:00",
                "2020-01-01 06:00:00",
            ],
        ),
        (
            "2023", "12", "25", "10", "00", "00",
            "2023", "12", "25", "13", "00", "00",
            0, 1,
            [
                "2023-12-25 10:00:00",
                "2023-12-25 11:00:00",
                "2023-12-25 12:00:00",
            ],
        ),
        (
            "2024", "03", "01", "00", "00", "00",
            "2024", "03", "08", "00", "00", "00",
            1, 12,
            [
                "2024-03-01 00:00:00",
                "2024-03-01 12:00:00",
                "2024-03-02 00:00:00",
                "2024-03-02 12:00:00",
                "2024-03-03 00:00:00",
                "2024-03-03 12:00:00",
                "2024-03-04 00:00:00",
                "2024-03-04 12:00:00",
                "2024-03-05 00:00:00",
                "2024-03-05 12:00:00",
                "2024-03-06 00:00:00",
                "2024-03-06 12:00:00",
                "2024-03-07 00:00:00",
                "2024-03-07 12:00:00",
            ],
        ),
        # Add more future datasets here by defining different start and end times
        # and time deltas.
    ],
)
def test_datetime_data(
    start_year, start_month, start_day, start_hour, start_minute, start_second,
    end_year, end_month, end_day, end_hour, end_minute, end_second,
    time_delta_days, time_delta_hours, expected_data
):
    result = dd.datetime_data(
        start_year=start_year,
        start_month=start_month,
        start_day=start_day,
        start_hour=start_hour,
        start_minute=start_minute,
        start_second=start_second,
        end_year=end_year,
        end_month=end_month,
        end_day=end_day,
        end_hour=end_hour,
        end_minute=end_minute,
        end_second=end_second,
        time_delta_days=time_delta_days,
        time_delta_hours=time_delta_hours,
    )
    expected = pd.Series(data=expected_data).astype(dtype="datetime64[s]")
    assert result.equals(other=expected)


def test_timedelta_data():
    result = dd.timedelta_data(time_delta_days=7)
    expected = pd.Series(
        data=[0, 0, 0, 0, 0, 0, 0, 0]
    ).astype(dtype="timedelta64[s]")
    assert result.equals(other=expected)


@mark.parametrize(
    "hypothesized_value, alternative_hypothesis, expected",
    [
        (
            400,
            "two-sided",
            (
                -2.2519472501384548,
                0.0337482297588424,
                0.5798034164658731,
                0.9746973097386498,
                0.7642839483945643,
                0.2270875306568172,
                0.703,
                0.1009686916604779,
                0.7255204234760189,
                266.91858206241807,
                394.20141793758194,
            ),
        ),
        (
            400,
            "less",
            (
                -2.2519472501384548,
                0.0168741148794212,
                6.257488453142133e-05,
                0.9746973097386498,
                0.7642839483945643,
                0.2270875306568172,
                0.703,
                0.1009686916604779,
                0.7255204234760189,
                "N/A",
                383.3159655856088,
            ),
        ),
        (
            400,
            "greater",
            (
                -2.2519472501384548,
                0.9831258851205789,
                0.7063989742605766,
                0.9746973097386498,
                0.7642839483945643,
                0.2270875306568172,
                0.703,
                0.1009686916604779,
                0.7255204234760189,
                277.8040344143912,
                "N/A",
            ),
        ),
    ],
)
def test_one_sample_t(hypothesized_value, alternative_hypothesis, expected):
    result = dd.one_sample_t(
        series=series_one_sample_t,
        hypothesized_value=hypothesized_value,
        alternative_hypothesis=alternative_hypothesis,
    )
    assert result == expected


@mark.parametrize(
    "alternative_hypothesis, significance_level, expected",
    [
        (
            "two-sided",
            0.05,
            (
                2.1353336482435243,
                0.0467302735601054,
                0.5243039932709265,
                0.9785249763729523,
                0.9574032744427222,
                0.8853149752492473,
                0.17846557720076883,
                3.2744574205759416,
                0.07036619072494953,
                0.15265397324961683,
                0.68,
                0.49940696863048295,
                0.693,
                0.06234516845619442,
                7.67502856891755,
            ),
        ),
        (
            "less",
            0.05,
            (
                2.1353336482435243,
                0.9766348632199473,
                0.00010611922933968093,
                0.9785249763729523,
                0.9574032744427222,
                0.8853149752492473,
                0.17846557720076883,
                3.2744574205759416,
                0.07036619072494953,
                0.15265397324961683,
                0.68,
                0.49940696863048295,
                0.693,
                0.06234516845619442,
                7.67502856891755,
            ),
        ),
        (
            "greater",
            0.05,
            (
                2.1353336482435243,
                0.0233651367800527,
                0.6587984489683615,
                0.9785249763729523,
                0.9574032744427222,
                0.8853149752492473,
                0.17846557720076883,
                3.2744574205759416,
                0.07036619072494953,
                0.15265397324961683,
                0.68,
                0.49940696863048295,
                0.693,
                0.06234516845619442,
                7.67502856891755,
            ),
        ),
    ],
)
def test_two_sample_t(alternative_hypothesis, significance_level, expected):
    result = dd.two_sample_t(
        series1=series1_two_sample_t,
        series2=series2_two_sample_t,
        alternative_hypothesis=alternative_hypothesis,
        significance_level=significance_level,
    )
    assert result == expected
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic sample 1, Shapiro-Wilk p value sample 1,
    # Shapiro-Wilk statistic sample 2, Shapiro-Wilk p value sample 2,
    # Bartlett test statistic, Bartlett p value,
    # Anderson-Darling test statistic, Anderson-Darling p value`
    # )


def test_paired_t():
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="two-sided",
    )
    # expected = (
    # t statistic, t p value, t power,
    # Shapiro-Wilk statistic, Shapiro-Wilk p value,
    # Anderson-Darling test statistic, Anderson-Darling p value
    # )
    expected = (
        3.0234339882840073,
        0.006989193823492975,
        0.9718569087171878,
        0.7935152200395024,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.6770122524449045,
        3.722987747555096,
    )
    assert result == expected
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="less",
    )
    expected = (
        3.0234339882840073,
        0.9965054030882535,
        0.9718569087171878,
        0.7935152200395024,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.9417975057209451,
        3.458202494279055,
    )
    assert result == expected
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="greater",
    )
    expected = (
        3.0234339882840073,
        0.0034945969117464873,
        0.9718567132949829,
        0.7935113906860352,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.9417975057209451,
        3.458202494279055,
    )
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="two-sided",
        hypothesized_value=4,
    )
    expected = (
        -2.4737187176869146,
        0.022976718604245508,
        0.9718569087171878,
        0.7935152200395024,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.6770122524449045,
        3.722987747555096,
    )
    assert result == expected
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="less",
        hypothesized_value=4,
    )
    expected = (
        -2.4737187176869146,
        0.011488359302122775,
        0.9718569087171878,
        0.7935152200395024,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.9417975057209451,
        3.458202494279055,
    )
    assert result == expected
    result = dd.paired_t(
        series1=series1_paired,
        series2=series2_paired,
        significance_level=0.05,
        alternative_hypothesis="greater",
        hypothesized_value=4,
    )
    expected = (
        -2.4737187176869146,
        0.9885116406978772,
        0.9718569087171878,
        0.7935152200395024,
        0.33171651643374744,
        0.692,
        0.14709700945048904,
        0.3071349516596349,
        0.9417975057209451,
        3.458202494279055,
    )
    assert result == expected


def test_linear_regression():
    (
        fitted_model,
        predictions,
        confidence_interval_lower,
        confidence_interval_upper,
        prediction_interval_lower,
        prediction_interval_upper,
    ) = dd.linear_regression(
        X=df_linear_regression["X"],
        y=df_linear_regression["y"],
    )
    predictions = pd.Series(data=predictions).round(decimals=6)
    expected_predictions = pd.Series(
        data=[
            8.001000,
            7.000818,
            9.501273,
            7.500909,
            8.501091,
            10.001364,
            6.000636,
            5.000455,
            9.001182,
            6.500727,
            5.500545,
        ]
    ).round(decimals=6)
    assert predictions.equals(other=expected_predictions)
