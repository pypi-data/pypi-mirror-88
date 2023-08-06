***********************
Doctest of merge_curves
***********************

Merge curves is an essential function. It shown weird behavior in which an
value of one curve was added to all other curves.

Test with group 10
==================

Group 10 has 5 source curves.

.. testcode::

    >>> from arithmeticmeancurve import merge_set_of_curves_to_family
            >>> import examplecurves
            >>> from doctestprinter import doctest_iter_print, doctest_print
            >>> sample_curves = examplecurves.get(group_name="10")
            >>> doctest_iter_print(sample_curves)
                         y
            x
            0.00   0.00000
            1.15   1.40625
            2.30   2.70000
            3.45   3.88125
            4.60   4.95000
            5.75   5.90625
            6.90   6.75000
            8.05   7.48125
            9.20   8.10000
            10.35  8.60625
            11.50  9.00000
                        y
            x
            0.0    0.0000
            1.0    1.5625
            2.0    3.0000
            3.0    4.3125
            4.0    5.5000
            5.0    6.5625
            6.0    7.5000
            7.0    8.3125
            8.0    9.0000
            9.0    9.5625
            10.0  10.0000
                           y
            x
            0.00    0.000000
            1.01    1.640625
            2.02    3.150000
            3.03    4.528125
            4.04    5.775000
            5.05    6.890625
            6.06    7.875000
            7.07    8.728125
            8.08    9.450000
            9.09   10.040625
            10.10  10.500000
                          y
            x
            0.00   0.000000
            0.96   1.796875
            1.92   3.450000
            2.88   4.959375
            3.84   6.325000
            4.80   7.546875
            5.76   8.625000
            6.72   9.559375
            7.68  10.350000
            8.64  10.996875
            9.60  11.500000
                         y
            x
            0.0   0.000000
            0.9   1.796875
            1.8   3.450000
            2.7   4.959375
            3.6   6.325000
            4.5   7.546875
            5.4   8.625000
            6.3   9.559375
            7.2  10.350000
            8.1  10.996875
            9.0  11.500000
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print, doctest_print
        >>> sample_curves = examplecurves.get(group_name="10")
        >>> doctest_iter_print(sample_curves)
                     y
        x
        0.00   0.00000
        1.15   1.40625
        2.30   2.70000
        3.45   3.88125
        4.60   4.95000
        5.75   5.90625
        6.90   6.75000
        8.05   7.48125
        9.20   8.10000
        10.35  8.60625
        11.50  9.00000
                    y
        x
        0.0    0.0000
        1.0    1.5625
        2.0    3.0000
        3.0    4.3125
        4.0    5.5000
        5.0    6.5625
        6.0    7.5000
        7.0    8.3125
        8.0    9.0000
        9.0    9.5625
        10.0  10.0000
                       y
        x
        0.00    0.000000
        1.01    1.640625
        2.02    3.150000
        3.03    4.528125
        4.04    5.775000
        5.05    6.890625
        6.06    7.875000
        7.07    8.728125
        8.08    9.450000
        9.09   10.040625
        10.10  10.500000
                      y
        x
        0.00   0.000000
        0.96   1.796875
        1.92   3.450000
        2.88   4.959375
        3.84   6.325000
        4.80   7.546875
        5.76   8.625000
        6.72   9.559375
        7.68  10.350000
        8.64  10.996875
        9.60  11.500000
                     y
        x
        0.0   0.000000
        0.9   1.796875
        1.8   3.450000
        2.7   4.959375
        3.6   6.325000
        4.5   7.546875
        5.4   8.625000
        6.3   9.559375
        7.2  10.350000
        8.1  10.996875
        9.0  11.500000
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print, doctest_print
        >>> sample_curves = examplecurves.get(group_name="10")
        >>> doctest_iter_print(sample_curves)
                     y
        x
        0.00   0.00000
        1.15   1.40625
        2.30   2.70000
        3.45   3.88125
        4.60   4.95000
        5.75   5.90625
        6.90   6.75000
        8.05   7.48125
        9.20   8.10000
        10.35  8.60625
        11.50  9.00000
                    y
        x
        0.0    0.0000
        1.0    1.5625
        2.0    3.0000
        3.0    4.3125
        4.0    5.5000
        5.0    6.5625
        6.0    7.5000
        7.0    8.3125
        8.0    9.0000
        9.0    9.5625
        10.0  10.0000
                       y
        x
        0.00    0.000000
        1.01    1.640625
        2.02    3.150000
        3.03    4.528125
        4.04    5.775000
        5.05    6.890625
        6.06    7.875000
        7.07    8.728125
        8.08    9.450000
        9.09   10.040625
        10.10  10.500000
                      y
        x
        0.00   0.000000
        0.96   1.796875
        1.92   3.450000
        2.88   4.959375
        3.84   6.325000
        4.80   7.546875
        5.76   8.625000
        6.72   9.559375
        7.68  10.350000
        8.64  10.996875
        9.60  11.500000
                     y
        x
        0.0   0.000000
        0.9   1.796875
        1.8   3.450000
        2.7   4.959375
        3.6   6.325000
        4.5   7.546875
        5.4   8.625000
        6.3   9.559375
        7.2  10.350000
        8.1  10.996875
        9.0  11.500000
    >>> import examplecurves
    >>> from doctestprinter import doctest_iter_print, doctest_print
    >>> sample_curves = examplecurves.get(group_name="10")
    >>> doctest_iter_print(sample_curves)
                 y
    x
    0.00   0.00000
    1.15   1.40625
    2.30   2.70000
    3.45   3.88125
    4.60   4.95000
    5.75   5.90625
    6.90   6.75000
    8.05   7.48125
    9.20   8.10000
    10.35  8.60625
    11.50  9.00000
                y
    x
    0.0    0.0000
    1.0    1.5625
    2.0    3.0000
    3.0    4.3125
    4.0    5.5000
    5.0    6.5625
    6.0    7.5000
    7.0    8.3125
    8.0    9.0000
    9.0    9.5625
    10.0  10.0000
                   y
    x
    0.00    0.000000
    1.01    1.640625
    2.02    3.150000
    3.03    4.528125
    4.04    5.775000
    5.05    6.890625
    6.06    7.875000
    7.07    8.728125
    8.08    9.450000
    9.09   10.040625
    10.10  10.500000
                  y
    x
    0.00   0.000000
    0.96   1.796875
    1.92   3.450000
    2.88   4.959375
    3.84   6.325000
    4.80   7.546875
    5.76   8.625000
    6.72   9.559375
    7.68  10.350000
    8.64  10.996875
    9.60  11.500000
                 y
    x
    0.0   0.000000
    0.9   1.796875
    1.8   3.450000
    2.7   4.959375
    3.6   6.325000
    4.5   7.546875
    5.4   8.625000
    6.3   9.559375
    7.2  10.350000
    8.1  10.996875
    9.0  11.500000

.. testcode::

    >>> from arithmeticmeancurve import merge_two_curves
        >>> first_left = sample_curves[0].copy()
        >>> second_right = sample_curves[1].copy()
        >>> first_left.columns = ["y_0"]
        >>> second_right.columns = ["y_1"]
        >>> first_merge = _merge_two_curves(first_left, second_right)
        >>> doctest_print(first_merge)
                   y_0      y_1
        x
        0.00   0.00000   0.0000
        1.00       NaN   1.5625
        1.15   1.40625      NaN
        2.00       NaN   3.0000
        2.30   2.70000      NaN
        3.00       NaN   4.3125
        3.45   3.88125      NaN
        4.00       NaN   5.5000
        4.60   4.95000      NaN
        5.00       NaN   6.5625
        5.75   5.90625      NaN
        6.00       NaN   7.5000
        6.90   6.75000      NaN
        7.00       NaN   8.3125
        8.00       NaN   9.0000
        8.05   7.48125      NaN
        9.00       NaN   9.5625
        9.20   8.10000      NaN
        10.00      NaN  10.0000
        10.35  8.60625      NaN
        11.50  9.00000      NaN
    >>> first_left = sample_curves[0].copy()
    >>> second_right = sample_curves[1].copy()
    >>> first_left.columns = ["y_0"]
    >>> second_right.columns = ["y_1"]
    >>> first_merge = merge_two_curves(first_left, second_right)
    >>> doctest_print(first_merge)
               y_0      y_1
    x
    0.00   0.00000   0.0000
    1.00       NaN   1.5625
    1.15   1.40625      NaN
    2.00       NaN   3.0000
    2.30   2.70000      NaN
    3.00       NaN   4.3125
    3.45   3.88125      NaN
    4.00       NaN   5.5000
    4.60   4.95000      NaN
    5.00       NaN   6.5625
    5.75   5.90625      NaN
    6.00       NaN   7.5000
    6.90   6.75000      NaN
    7.00       NaN   8.3125
    8.00       NaN   9.0000
    8.05   7.48125      NaN
    9.00       NaN   9.5625
    9.20   8.10000      NaN
    10.00      NaN  10.0000
    10.35  8.60625      NaN
    11.50  9.00000      NaN

.. testcode::

    >>> from arithmeticmeancurve import merge_two_curves
        >>> third_right = sample_curves[2].copy()
        >>> third_right.columns = ["y_2"]
        >>> second_merge = _merge_two_curves(first_merge, third_right)
        >>> doctest_print(second_merge)
                   y_0      y_1        y_2
        x
        0.00   0.00000   0.0000   0.000000
        1.00       NaN   1.5625        NaN
        1.01       NaN      NaN   1.640625
        1.15   1.40625      NaN        NaN
        2.00       NaN   3.0000        NaN
        2.02       NaN      NaN   3.150000
        2.30   2.70000      NaN        NaN
        3.00       NaN   4.3125        NaN
        3.03       NaN      NaN   4.528125
        3.45   3.88125      NaN        NaN
        4.00       NaN   5.5000        NaN
        4.04       NaN      NaN   5.775000
        4.60   4.95000      NaN        NaN
        5.00       NaN   6.5625        NaN
        5.05       NaN      NaN   6.890625
        5.75   5.90625      NaN        NaN
        6.00       NaN   7.5000        NaN
        6.06       NaN      NaN   7.875000
        6.90   6.75000      NaN        NaN
        7.00       NaN   8.3125        NaN
        7.07       NaN      NaN   8.728125
        8.00       NaN   9.0000        NaN
        8.05   7.48125      NaN        NaN
        8.08       NaN      NaN   9.450000
        9.00       NaN   9.5625        NaN
        9.09       NaN      NaN  10.040625
        9.20   8.10000      NaN        NaN
        10.00      NaN  10.0000        NaN
        10.10      NaN      NaN  10.500000
        10.35  8.60625      NaN        NaN
        11.50  9.00000      NaN        NaN
    >>> third_right = sample_curves[2].copy()
    >>> third_right.columns = ["y_2"]
    >>> second_merge = merge_two_curves(first_merge, third_right)
    >>> doctest_print(second_merge)
               y_0      y_1        y_2
    x
    0.00   0.00000   0.0000   0.000000
    1.00       NaN   1.5625        NaN
    1.01       NaN      NaN   1.640625
    1.15   1.40625      NaN        NaN
    2.00       NaN   3.0000        NaN
    2.02       NaN      NaN   3.150000
    2.30   2.70000      NaN        NaN
    3.00       NaN   4.3125        NaN
    3.03       NaN      NaN   4.528125
    3.45   3.88125      NaN        NaN
    4.00       NaN   5.5000        NaN
    4.04       NaN      NaN   5.775000
    4.60   4.95000      NaN        NaN
    5.00       NaN   6.5625        NaN
    5.05       NaN      NaN   6.890625
    5.75   5.90625      NaN        NaN
    6.00       NaN   7.5000        NaN
    6.06       NaN      NaN   7.875000
    6.90   6.75000      NaN        NaN
    7.00       NaN   8.3125        NaN
    7.07       NaN      NaN   8.728125
    8.00       NaN   9.0000        NaN
    8.05   7.48125      NaN        NaN
    8.08       NaN      NaN   9.450000
    9.00       NaN   9.5625        NaN
    9.09       NaN      NaN  10.040625
    9.20   8.10000      NaN        NaN
    10.00      NaN  10.0000        NaN
    10.10      NaN      NaN  10.500000
    10.35  8.60625      NaN        NaN
    11.50  9.00000      NaN        NaN


.. testcode::

    >>> from arithmeticmeancurve import merge_two_curves
        >>> fourth_right = sample_curves[3].copy()
        >>> fourth_right.columns = ["y_3"]
        >>> third_merge = _merge_two_curves(second_merge, fourth_right)
        >>> doctest_print(third_merge)
                   y_0      y_1        y_2        y_3
        x
        0.00   0.00000   0.0000   0.000000   0.000000
        0.96       NaN      NaN        NaN   1.796875
        1.00       NaN   1.5625        NaN        NaN
        1.01       NaN      NaN   1.640625        NaN
        1.15   1.40625      NaN        NaN        NaN
        1.92       NaN      NaN        NaN   3.450000
        2.00       NaN   3.0000        NaN        NaN
        2.02       NaN      NaN   3.150000        NaN
        2.30   2.70000      NaN        NaN        NaN
        2.88       NaN      NaN        NaN   4.959375
        3.00       NaN   4.3125        NaN        NaN
        3.03       NaN      NaN   4.528125        NaN
        3.45   3.88125      NaN        NaN        NaN
        3.84       NaN      NaN        NaN   6.325000
        4.00       NaN   5.5000        NaN        NaN
        4.04       NaN      NaN   5.775000        NaN
        4.60   4.95000      NaN        NaN        NaN
        4.80       NaN      NaN        NaN   7.546875
        5.00       NaN   6.5625        NaN        NaN
        5.05       NaN      NaN   6.890625        NaN
        5.75   5.90625      NaN        NaN        NaN
        5.76       NaN      NaN        NaN   8.625000
        6.00       NaN   7.5000        NaN        NaN
        6.06       NaN      NaN   7.875000        NaN
        6.72       NaN      NaN        NaN   9.559375
        6.90   6.75000      NaN        NaN        NaN
        7.00       NaN   8.3125        NaN        NaN
        7.07       NaN      NaN   8.728125        NaN
        7.68       NaN      NaN        NaN  10.350000
        8.00       NaN   9.0000        NaN        NaN
        8.05   7.48125      NaN        NaN        NaN
        8.08       NaN      NaN   9.450000        NaN
        8.64       NaN      NaN        NaN  10.996875
        9.00       NaN   9.5625        NaN        NaN
        9.09       NaN      NaN  10.040625        NaN
        9.20   8.10000      NaN        NaN        NaN
        9.60       NaN      NaN        NaN  11.500000
        10.00      NaN  10.0000        NaN        NaN
        10.10      NaN      NaN  10.500000        NaN
        10.35  8.60625      NaN        NaN        NaN
        11.50  9.00000      NaN        NaN        NaN

    The final merge lead to an incorrect result with the following
    rows within the resulting DataFrame. At the index '9.0' the
    curves
    >>> fourth_right = sample_curves[3].copy()
    >>> fourth_right.columns = ["y_3"]
    >>> third_merge = merge_two_curves(second_merge, fourth_right)
    >>> doctest_print(third_merge)
               y_0      y_1        y_2        y_3
    x
    0.00   0.00000   0.0000   0.000000   0.000000
    0.96       NaN      NaN        NaN   1.796875
    1.00       NaN   1.5625        NaN        NaN
    1.01       NaN      NaN   1.640625        NaN
    1.15   1.40625      NaN        NaN        NaN
    1.92       NaN      NaN        NaN   3.450000
    2.00       NaN   3.0000        NaN        NaN
    2.02       NaN      NaN   3.150000        NaN
    2.30   2.70000      NaN        NaN        NaN
    2.88       NaN      NaN        NaN   4.959375
    3.00       NaN   4.3125        NaN        NaN
    3.03       NaN      NaN   4.528125        NaN
    3.45   3.88125      NaN        NaN        NaN
    3.84       NaN      NaN        NaN   6.325000
    4.00       NaN   5.5000        NaN        NaN
    4.04       NaN      NaN   5.775000        NaN
    4.60   4.95000      NaN        NaN        NaN
    4.80       NaN      NaN        NaN   7.546875
    5.00       NaN   6.5625        NaN        NaN
    5.05       NaN      NaN   6.890625        NaN
    5.75   5.90625      NaN        NaN        NaN
    5.76       NaN      NaN        NaN   8.625000
    6.00       NaN   7.5000        NaN        NaN
    6.06       NaN      NaN   7.875000        NaN
    6.72       NaN      NaN        NaN   9.559375
    6.90   6.75000      NaN        NaN        NaN
    7.00       NaN   8.3125        NaN        NaN
    7.07       NaN      NaN   8.728125        NaN
    7.68       NaN      NaN        NaN  10.350000
    8.00       NaN   9.0000        NaN        NaN
    8.05   7.48125      NaN        NaN        NaN
    8.08       NaN      NaN   9.450000        NaN
    8.64       NaN      NaN        NaN  10.996875
    9.00       NaN   9.5625        NaN        NaN
    9.09       NaN      NaN  10.040625        NaN
    9.20   8.10000      NaN        NaN        NaN
    9.60       NaN      NaN        NaN  11.500000
    10.00      NaN  10.0000        NaN        NaN
    10.10      NaN      NaN  10.500000        NaN
    10.35  8.60625      NaN        NaN        NaN
    11.50  9.00000      NaN        NaN        NaN

The final merge lead to an incorrect result with the following
rows within the resulting DataFrame. At the index '9.0' the
curves *y_0* - *y_3* got their value wrongfully overridden.

..

                y_0      y_1        y_2        y_3        y_4
    x
    0.00    0.00000   0.0000   0.000000   0.000000   0.000000
    ...
    8.64        NaN      NaN        NaN  10.996875        NaN
    9.00   11.50000  11.5000  11.500000  11.500000  11.500000
    9.09        NaN      NaN  10.040625        NaN        NaN
    ...

.. testcode::

    >>> from arithmeticmeancurve import merge_curves
        >>> pre_merge = merge_family_of_curves(sample_curves[:4])
        >>> fifth_right = sample_curves[4].copy()
        >>> final_merge = merge_two_curves(pre_merge, fifth_right, copy_at_concat=False)
        >>> from doctestprinter import doctest_print
        >>> _debug_condition = "merge_two_curve group 10 test 0"
        >>> doctest_print(final_merge.iloc[40:46])
              y_0     y_1        y_2        y_3          y
        x
        8.10  NaN     NaN        NaN        NaN  10.996875
        8.64  NaN     NaN        NaN  10.996875        NaN
        9.00  NaN  9.5625        NaN        NaN  11.500000
        9.09  NaN     NaN  10.040625        NaN        NaN
        9.20  8.1     NaN        NaN        NaN        NaN
        9.60  NaN     NaN        NaN  11.500000        NaN
    >>> pre_merge = merge_curves(sample_curves[:4])
    >>> fifth_right = sample_curves[4].copy()
    >>> final_merge = merge_two_curves(pre_merge, fifth_right, copy_at_concat=False)
    >>> from doctestprinter import doctest_print
    >>> _debug_condition = "merge_two_curve group 10 test 0"
    >>> doctest_print(final_merge.iloc[40:46])
          y_0     y_1        y_2        y_3          y
    x
    8.10  NaN     NaN        NaN        NaN  10.996875
    8.64  NaN     NaN        NaN  10.996875        NaN
    9.00  NaN  9.5625        NaN        NaN  11.500000
    9.09  NaN     NaN  10.040625        NaN        NaN
    9.20  8.1     NaN        NaN        NaN        NaN
    9.60  NaN     NaN        NaN  11.500000        NaN



.. testcode::

    >>> from arithmeticmeancurve import merge_set_of_curves_to_family
            >>> merged_sample = merge_curves(sample_curves)
            >>> from doctestprinter import doctest_print
            >>> doctest_print(merged_sample)
                       y_0      y_1        y_2        y_3        y_4
            x
            0.00   0.00000   0.0000   0.000000   0.000000   0.000000
            0.90       NaN      NaN        NaN        NaN   1.796875
            0.96       NaN      NaN        NaN   1.796875        NaN
            1.00       NaN   1.5625        NaN        NaN        NaN
            1.01       NaN      NaN   1.640625        NaN        NaN
            1.15   1.40625      NaN        NaN        NaN        NaN
            1.80       NaN      NaN        NaN        NaN   3.450000
            1.92       NaN      NaN        NaN   3.450000        NaN
            2.00       NaN   3.0000        NaN        NaN        NaN
            2.02       NaN      NaN   3.150000        NaN        NaN
            2.30   2.70000      NaN        NaN        NaN        NaN
            2.70       NaN      NaN        NaN        NaN   4.959375
            2.88       NaN      NaN        NaN   4.959375        NaN
            3.00       NaN   4.3125        NaN        NaN        NaN
            3.03       NaN      NaN   4.528125        NaN        NaN
            3.45   3.88125      NaN        NaN        NaN        NaN
            3.60       NaN      NaN        NaN        NaN   6.325000
            3.84       NaN      NaN        NaN   6.325000        NaN
            4.00       NaN   5.5000        NaN        NaN        NaN
            4.04       NaN      NaN   5.775000        NaN        NaN
            4.50       NaN      NaN        NaN        NaN   7.546875
            4.60   4.95000      NaN        NaN        NaN        NaN
            4.80       NaN      NaN        NaN   7.546875        NaN
            5.00       NaN   6.5625        NaN        NaN        NaN
            5.05       NaN      NaN   6.890625        NaN        NaN
            5.40       NaN      NaN        NaN        NaN   8.625000
            5.75   5.90625      NaN        NaN        NaN        NaN
            5.76       NaN      NaN        NaN   8.625000        NaN
            6.00       NaN   7.5000        NaN        NaN        NaN
            6.06       NaN      NaN   7.875000        NaN        NaN
            6.30       NaN      NaN        NaN        NaN   9.559375
            6.72       NaN      NaN        NaN   9.559375        NaN
            6.90   6.75000      NaN        NaN        NaN        NaN
            7.00       NaN   8.3125        NaN        NaN        NaN
            7.07       NaN      NaN   8.728125        NaN        NaN
            7.20       NaN      NaN        NaN        NaN  10.350000
            7.68       NaN      NaN        NaN  10.350000        NaN
            8.00       NaN   9.0000        NaN        NaN        NaN
            8.05   7.48125      NaN        NaN        NaN        NaN
            8.08       NaN      NaN   9.450000        NaN        NaN
            8.10       NaN      NaN        NaN        NaN  10.996875
            8.64       NaN      NaN        NaN  10.996875        NaN
            9.00       NaN   9.5625        NaN        NaN  11.500000
            9.09       NaN      NaN  10.040625        NaN        NaN
            9.20   8.10000      NaN        NaN        NaN        NaN
            9.60       NaN      NaN        NaN  11.500000        NaN
            10.00      NaN  10.0000        NaN        NaN        NaN
            10.10      NaN      NaN  10.500000        NaN        NaN
            10.35  8.60625      NaN        NaN        NaN        NaN
            11.50  9.00000      NaN        NaN        NaN        NaN
        >>> merged_sample = merge_curves(sample_curves)
        >>> from doctestprinter import doctest_print
        >>> doctest_print(merged_sample)
                   y_0      y_1        y_2        y_3        y_4
        x
        0.00   0.00000   0.0000   0.000000   0.000000   0.000000
        0.90       NaN      NaN        NaN        NaN   1.796875
        0.96       NaN      NaN        NaN   1.796875        NaN
        1.00       NaN   1.5625        NaN        NaN        NaN
        1.01       NaN      NaN   1.640625        NaN        NaN
        1.15   1.40625      NaN        NaN        NaN        NaN
        1.80       NaN      NaN        NaN        NaN   3.450000
        1.92       NaN      NaN        NaN   3.450000        NaN
        2.00       NaN   3.0000        NaN        NaN        NaN
        2.02       NaN      NaN   3.150000        NaN        NaN
        2.30   2.70000      NaN        NaN        NaN        NaN
        2.70       NaN      NaN        NaN        NaN   4.959375
        2.88       NaN      NaN        NaN   4.959375        NaN
        3.00       NaN   4.3125        NaN        NaN        NaN
        3.03       NaN      NaN   4.528125        NaN        NaN
        3.45   3.88125      NaN        NaN        NaN        NaN
        3.60       NaN      NaN        NaN        NaN   6.325000
        3.84       NaN      NaN        NaN   6.325000        NaN
        4.00       NaN   5.5000        NaN        NaN        NaN
        4.04       NaN      NaN   5.775000        NaN        NaN
        4.50       NaN      NaN        NaN        NaN   7.546875
        4.60   4.95000      NaN        NaN        NaN        NaN
        4.80       NaN      NaN        NaN   7.546875        NaN
        5.00       NaN   6.5625        NaN        NaN        NaN
        5.05       NaN      NaN   6.890625        NaN        NaN
        5.40       NaN      NaN        NaN        NaN   8.625000
        5.75   5.90625      NaN        NaN        NaN        NaN
        5.76       NaN      NaN        NaN   8.625000        NaN
        6.00       NaN   7.5000        NaN        NaN        NaN
        6.06       NaN      NaN   7.875000        NaN        NaN
        6.30       NaN      NaN        NaN        NaN   9.559375
        6.72       NaN      NaN        NaN   9.559375        NaN
        6.90   6.75000      NaN        NaN        NaN        NaN
        7.00       NaN   8.3125        NaN        NaN        NaN
        7.07       NaN      NaN   8.728125        NaN        NaN
        7.20       NaN      NaN        NaN        NaN  10.350000
        7.68       NaN      NaN        NaN  10.350000        NaN
        8.00       NaN   9.0000        NaN        NaN        NaN
        8.05   7.48125      NaN        NaN        NaN        NaN
        8.08       NaN      NaN   9.450000        NaN        NaN
        8.10       NaN      NaN        NaN        NaN  10.996875
        8.64       NaN      NaN        NaN  10.996875        NaN
        9.00       NaN   9.5625        NaN        NaN  11.500000
        9.09       NaN      NaN  10.040625        NaN        NaN
        9.20   8.10000      NaN        NaN        NaN        NaN
        9.60       NaN      NaN        NaN  11.500000        NaN
        10.00      NaN  10.0000        NaN        NaN        NaN
        10.10      NaN      NaN  10.500000        NaN        NaN
        10.35  8.60625      NaN        NaN        NaN        NaN
        11.50  9.00000      NaN        NaN        NaN        NaN
        >>> merged_sample = merge_curves(sample_curves)
        >>> from doctestprinter import doctest_print
        >>> doctest_print(merged_sample)
                   y_0      y_1        y_2        y_3        y_4
        x
        0.00   0.00000   0.0000   0.000000   0.000000   0.000000
        0.90       NaN      NaN        NaN        NaN   1.796875
        0.96       NaN      NaN        NaN   1.796875        NaN
        1.00       NaN   1.5625        NaN        NaN        NaN
        1.01       NaN      NaN   1.640625        NaN        NaN
        1.15   1.40625      NaN        NaN        NaN        NaN
        1.80       NaN      NaN        NaN        NaN   3.450000
        1.92       NaN      NaN        NaN   3.450000        NaN
        2.00       NaN   3.0000        NaN        NaN        NaN
        2.02       NaN      NaN   3.150000        NaN        NaN
        2.30   2.70000      NaN        NaN        NaN        NaN
        2.70       NaN      NaN        NaN        NaN   4.959375
        2.88       NaN      NaN        NaN   4.959375        NaN
        3.00       NaN   4.3125        NaN        NaN        NaN
        3.03       NaN      NaN   4.528125        NaN        NaN
        3.45   3.88125      NaN        NaN        NaN        NaN
        3.60       NaN      NaN        NaN        NaN   6.325000
        3.84       NaN      NaN        NaN   6.325000        NaN
        4.00       NaN   5.5000        NaN        NaN        NaN
        4.04       NaN      NaN   5.775000        NaN        NaN
        4.50       NaN      NaN        NaN        NaN   7.546875
        4.60   4.95000      NaN        NaN        NaN        NaN
        4.80       NaN      NaN        NaN   7.546875        NaN
        5.00       NaN   6.5625        NaN        NaN        NaN
        5.05       NaN      NaN   6.890625        NaN        NaN
        5.40       NaN      NaN        NaN        NaN   8.625000
        5.75   5.90625      NaN        NaN        NaN        NaN
        5.76       NaN      NaN        NaN   8.625000        NaN
        6.00       NaN   7.5000        NaN        NaN        NaN
        6.06       NaN      NaN   7.875000        NaN        NaN
        6.30       NaN      NaN        NaN        NaN   9.559375
        6.72       NaN      NaN        NaN   9.559375        NaN
        6.90   6.75000      NaN        NaN        NaN        NaN
        7.00       NaN   8.3125        NaN        NaN        NaN
        7.07       NaN      NaN   8.728125        NaN        NaN
        7.20       NaN      NaN        NaN        NaN  10.350000
        7.68       NaN      NaN        NaN  10.350000        NaN
        8.00       NaN   9.0000        NaN        NaN        NaN
        8.05   7.48125      NaN        NaN        NaN        NaN
        8.08       NaN      NaN   9.450000        NaN        NaN
        8.10       NaN      NaN        NaN        NaN  10.996875
        8.64       NaN      NaN        NaN  10.996875        NaN
        9.00       NaN   9.5625        NaN        NaN  11.500000
        9.09       NaN      NaN  10.040625        NaN        NaN
        9.20   8.10000      NaN        NaN        NaN        NaN
        9.60       NaN      NaN        NaN  11.500000        NaN
        10.00      NaN  10.0000        NaN        NaN        NaN
        10.10      NaN      NaN  10.500000        NaN        NaN
        10.35  8.60625      NaN        NaN        NaN        NaN
        11.50  9.00000      NaN        NaN        NaN        NaN
    >>> merged_sample = merge_curves(sample_curves)
    >>> from doctestprinter import doctest_print
    >>> doctest_print(merged_sample)
               y_0      y_1        y_2        y_3        y_4
    x
    0.00   0.00000   0.0000   0.000000   0.000000   0.000000
    0.90       NaN      NaN        NaN        NaN   1.796875
    0.96       NaN      NaN        NaN   1.796875        NaN
    1.00       NaN   1.5625        NaN        NaN        NaN
    1.01       NaN      NaN   1.640625        NaN        NaN
    1.15   1.40625      NaN        NaN        NaN        NaN
    1.80       NaN      NaN        NaN        NaN   3.450000
    1.92       NaN      NaN        NaN   3.450000        NaN
    2.00       NaN   3.0000        NaN        NaN        NaN
    2.02       NaN      NaN   3.150000        NaN        NaN
    2.30   2.70000      NaN        NaN        NaN        NaN
    2.70       NaN      NaN        NaN        NaN   4.959375
    2.88       NaN      NaN        NaN   4.959375        NaN
    3.00       NaN   4.3125        NaN        NaN        NaN
    3.03       NaN      NaN   4.528125        NaN        NaN
    3.45   3.88125      NaN        NaN        NaN        NaN
    3.60       NaN      NaN        NaN        NaN   6.325000
    3.84       NaN      NaN        NaN   6.325000        NaN
    4.00       NaN   5.5000        NaN        NaN        NaN
    4.04       NaN      NaN   5.775000        NaN        NaN
    4.50       NaN      NaN        NaN        NaN   7.546875
    4.60   4.95000      NaN        NaN        NaN        NaN
    4.80       NaN      NaN        NaN   7.546875        NaN
    5.00       NaN   6.5625        NaN        NaN        NaN
    5.05       NaN      NaN   6.890625        NaN        NaN
    5.40       NaN      NaN        NaN        NaN   8.625000
    5.75   5.90625      NaN        NaN        NaN        NaN
    5.76       NaN      NaN        NaN   8.625000        NaN
    6.00       NaN   7.5000        NaN        NaN        NaN
    6.06       NaN      NaN   7.875000        NaN        NaN
    6.30       NaN      NaN        NaN        NaN   9.559375
    6.72       NaN      NaN        NaN   9.559375        NaN
    6.90   6.75000      NaN        NaN        NaN        NaN
    7.00       NaN   8.3125        NaN        NaN        NaN
    7.07       NaN      NaN   8.728125        NaN        NaN
    7.20       NaN      NaN        NaN        NaN  10.350000
    7.68       NaN      NaN        NaN  10.350000        NaN
    8.00       NaN   9.0000        NaN        NaN        NaN
    8.05   7.48125      NaN        NaN        NaN        NaN
    8.08       NaN      NaN   9.450000        NaN        NaN
    8.10       NaN      NaN        NaN        NaN  10.996875
    8.64       NaN      NaN        NaN  10.996875        NaN
    9.00       NaN   9.5625        NaN        NaN  11.500000
    9.09       NaN      NaN  10.040625        NaN        NaN
    9.20   8.10000      NaN        NaN        NaN        NaN
    9.60       NaN      NaN        NaN  11.500000        NaN
    10.00      NaN  10.0000        NaN        NaN        NaN
    10.10      NaN      NaN  10.500000        NaN        NaN
    10.35  8.60625      NaN        NaN        NaN        NaN
    11.50  9.00000      NaN        NaN        NaN        NaN

