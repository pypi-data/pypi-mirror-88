***********
Basic Usage
***********

Installation
============

The module can be installed via pip.

.. code-block:: shell

    $ pip install arithmeticmeancurve

An optional module is examplecurves_, which was outsourced from *arithmeticmeancurves*.
Its purpose is to provide exemplary, reproducible families of curves for testing and
debugging.

.. _examplecurves: https://pypi.org/project/examplecurves/

.. code-block:: shell

    $ pip install examplecurves


Example
=======

A curve within `arithmeticmeancurve` is defined by a pandas.DataFrame. In the
current implementation ArithmeticMeanCurve will take a list of pandas.DataFrame
and merge all columns into a single representation for which a mean curve is
calculated. Therefore the provided DataFrame should represent the targeted
family of curves only.

.. plot:: pyplots/basic_usage_example.py
   :include-source:
