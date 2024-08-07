import dawgdad as dd


def test_pp():
    average = 0.11001
    std_devn = 0.868663
    sample_size = 40
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = dd.pp(
        average=average,
        std_devn=std_devn,
        sample_size=sample_size,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (1.5349258956964131, 1.1953921108301047, 1.873778000024199)
    assert result == expected


def test_ppk():
    average = 0.11001
    std_devn = 0.868663
    sample_size = 40
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = dd.ppk(
        average=average,
        std_devn=std_devn,
        sample_size=sample_size,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha,
        toler=6,
    )
    expected = (
        1.4927115962500226, 1.5771401951428037, 1.4927115962500226,
        1.1457133294762083, 1.8397098630238369
    )
    assert result == expected


def test_cp():
    average = 0.11001
    std_devn = 0.89312
    subgroup_size = 2
    number_subgroups = 39
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = dd.cp(
        average=average,
        std_devn=std_devn,
        subgroup_size=subgroup_size,
        number_subgroups=number_subgroups,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (1.4928938253911381, 1.141174267641542, 1.8439148118984439)
    assert result == expected
    average = 0.14063
    std_devn = .003680138
    subgroup_size = 5
    number_subgroups = 27
    lower_spec = .125
    upper_spec = .155
    alpha = 0.05
    result = dd.cp(
        average=average,
        std_devn=std_devn,
        subgroup_size=subgroup_size,
        number_subgroups=number_subgroups,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (1.3586447029975506, 1.1686155595120815, 1.548357434841817)
    assert result == expected


def test_cpk():
    average = 0.11001
    std_devn = 0.89312
    subgroup_size = 2
    number_subgroups = 39
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = dd.cpk(
        average=average,
        std_devn=std_devn,
        subgroup_size=subgroup_size,
        number_subgroups=number_subgroups,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha,
        toler=6,
    )
    expected = (
        1.4518355129583185, 1.533952137823958, 1.4518355129583185,
        1.0928917337156085, 1.8107792922010284
    )
    assert result == expected
    average = 0.14063
    std_devn = .003680138
    subgroup_size = 5
    number_subgroups = 27
    lower_spec = .125
    upper_spec = .155
    alpha = 0.05
    result = dd.cpk(
        average=average,
        std_devn=std_devn,
        subgroup_size=subgroup_size,
        number_subgroups=number_subgroups,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha,
        toler=6,
    )
    expected = (
        1.301581625471653, 1.4157077805234481, 1.301581625471653,
        1.0802101837381173, 1.5229530672051887
    )
    assert result == expected


def test_cpm():
    average = 0.11001
    std_devn = 0.868663
    sample_size = 40
    target = 0
    lower_spec = -4
    upper_spec = 4
    alpha = 0.05
    result = dd.cpm(
        average=average,
        std_devn=std_devn,
        sample_size= sample_size,
        target=target,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (1.5227631097133512, 1.2396924251472865)
    assert result == expected
    average = 68.7705
    std_devn = 12.4469
    sample_size = 100
    target = 70
    lower_spec = 40
    upper_spec = 100
    alpha = 0.05
    result = dd.cpm(
        average=average,
        std_devn=std_devn,
        sample_size= sample_size,
        target=target,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        alpha=alpha
    )
    expected = (0.7995217351828376, 0.7058035394758811)
    assert result == expected
