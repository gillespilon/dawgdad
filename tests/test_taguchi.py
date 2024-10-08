import dawgdad as dd


def test_taguchi_loss_function():
    """
    Calculate the ACU for the Taguchi Loss Function.
    """
    # off-centred process
    average = 4.66
    std_dev = 1.80
    target = 7.5
    cost = 0.25
    x = 15
    result = dd.taguchi_loss_function(
        average=average,
        std_dev=std_dev,
        target=target,
        cost=cost,
        x=x,
    )
    expected = 0.05024711111111111
    assert result == expected
    # centred process
    average = 7.5
    std_dev = 1.80
    target = 7.5
    cost = 0.25
    x = 15
    result = dd.taguchi_loss_function(
        average=average,
        std_dev=std_dev,
        target=target,
        cost=cost,
        x=x,
    )
    expected = 0.014400000000000001
    assert result == expected
