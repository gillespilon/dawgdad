"""
Automation functions
"""

from dawgdad import convert_seconds_to_hh_mm_ss


def fahrenheit_to_celsius_table(
    min_fahrenheit: int = 350,
    max_fahrenheit: int = 450,
    fahrenheit_increment: int = 5,
    rounding_increment: int = 5
) -> str:
    """
    Generates an HTML table of Fahrenheit to Celsius conversions.

    Parameters
    ----------
    min_fahrenheit: int = 350
        The minimum Fahrenheit temperature to include in the table.
    max_fahrenheit: int = 450
        The maximum Fahrenheit temperature to include in the table.
    fahrenheit_increment: int = 5
        The increment in Fahrenheit degrees between each row in the table.
    rounding_increment: int = 5
        The increment of rounding in the ones place value.

    Returns
    -------
    html_table: str
        An HTML table of Fahrenheit to Celsius conversions.

    Example
    -------

    >>> import dawgdad as dd
    >>> output_url = 'fahrenheit_to_celsius.html'
    >>> header_title = 'Fahrenheit to Celsius'
    >>> header_id = 'fahrenehit-to-celsius'
    >>> original_stdout = dd.html_begin(
    ...     output_url=output_url,
    ...     header_title=header_title,
    ...     header_id=header_id
    ... )
    >>> table = dd.fahrenheit_to_celsius_table()
    >>> print(table)
    >>> dd.html_end(
    ...     original_stdout=original_stdout,
    ...     output_url=output_url
    ... )
    """
    html_table = """
    <table>
      <tr>
        <th>Fahrenheit</th>
        <th>Celsius</th>
      </tr>
    """
    for fahrenheit in range(
        min_fahrenheit,
        max_fahrenheit + fahrenheit_increment,
        fahrenheit_increment
    ):
        celsius = (
            rounding_increment *
            round(((fahrenheit - 32) * 5 / 9) / rounding_increment)
        )
        html_table += """
        <tr>
          <td>{}</td>
          <td>{}</td>
        </tr>
        """.format(fahrenheit, celsius)
    html_table += """
    </table>
    """
    return html_table


def water_coffee_tea_milk(
    *,
    mugs_coffee: int = 2,
    cups_tea: int = 0,
    mugs_tea: int = 0,
    water_coffee_filter_mass: int = 150,
    water_tea_cup_mass: int = 400,
    water_tea_mug_mass: int = 300,
    water_coffee_mass: int = 220,
    milk_coffee_mass: int = 225,
    coffee_beans_mass: int = 20,
    time_1000_g_water: int = 340
) -> list[int]:
    """
    Calculate the mass of water and milk required for coffee mugs, tea cups,
    and tea mugs. All units are g.

    Parameters
    ----------
    mugs_coffee: int = 2,
        The number of coffee mugs.
    cups_tea: int = 0,
        The number of tea cups.
    mugs_tea: int = 0,
        The number of tea mugs.
    water_coffee_filter_mass: int = 150,
        The mass of water to wet one coffee filter.
    water_tea_cup_mass: int = 400,
        The mass of water for a tea cup.
    water_tea_mug_mass: int = 300,
        The mass of water for a coffee mug.
    water_coffee_mass: int = 220
        The mass of water to wet the coffee grindd.
    milk_coffee_mass: int = 150
        The mass of milk for one serving.`
    coffee_beans_mnass: int = 20
        The mass of coffee beans for one serving.
    time_1000_g_water: int =340
        The time to boil 1000 g of water at 8 on a 2300 W induction element.

    Returns
    -------
    list[int]
        A list of seven integers.

        - water: int
            The total amount of water to boil (g).
        - coffee_mug_water: int
            The amount of water for the coffee mugs (g).
        - coffee_filter_water: int
            The amount of water to wet the coffee filters (g).
        - tea_cup_water: int
            The amount of water for the tea cups (g).
        - tea_mug_water: int
            The amount of water for the tea mugs (g).
        - coffee_milk: int
            The mass of milk to foam (g).
        - coffee_mass: int
            The mass of coffee beans to grind (g).

    Examples
    --------

    >>> import dawgdad as dd
    >>> dd.water_coffee_tea_milk(
    ...     mugs_coffee=1,
    ...     cups_tea=0,
    ...     mugs_tea=0
    ... )
    (370, 220, 150, 0, 0, 150, 20, (0, 2, 5))

    >>> coffee_mug_water, coffee_filter_water = [
    ...     dd.water_coffee_tea_milk(
    ...         mugs_coffee=1,
    ...         cups_tea=0,
    ...         mugs_tea=0
    ...     )[i] for i in [1, 2]
    ... ]
    >>> print(coffee_mug_water, coffee_filter_water)
    220 150

    >>> all_coffee_water = dd.water_coffee_tea_milk(
    ...     mugs_coffee=1,
    ...     cups_tea=0,
    ...     mugs_tea=0
    ... )[0:3]
    >>> print(all_coffee_water)
    (370, 220, 150)
    """
    coffee_mug_water = mugs_coffee * water_coffee_mass
    coffee_filter_water = mugs_coffee * water_coffee_filter_mass
    tea_cup_water = cups_tea * water_tea_cup_mass
    tea_mug_water = mugs_tea * water_tea_mug_mass
    water = coffee_mug_water + coffee_filter_water + tea_cup_water + \
        tea_mug_water
    coffee_milk = mugs_coffee * milk_coffee_mass
    coffee_mass = mugs_coffee * coffee_beans_mass
    time_water = water * time_1000_g_water / 1000
    time_h_min_s = convert_seconds_to_hh_mm_ss(
        seconds=time_water
    )
    return (
        water, coffee_mug_water, coffee_filter_water, tea_cup_water,
        tea_mug_water, coffee_milk, coffee_mass, time_h_min_s
    )


__all__ = (
    "fahrenheit_to_celsius_table",
    "water_coffee_tea_milk",
)
