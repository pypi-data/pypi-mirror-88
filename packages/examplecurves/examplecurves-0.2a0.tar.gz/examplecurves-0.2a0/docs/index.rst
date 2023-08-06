.. arithmeticcurve documentation master file, created by
   sphinx-quickstart on Wed Nov 18 21:57:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to examplecurves's documentation!
=========================================

**examplecurves** is a module outsourced from arithmeticmeancurves_.
Its main purpose is to provide exemplary, reproducible families of curves for testing and
debugging purposes.

.. _arithmeticmeancurves: https://gitlab.com/david.scheliga/arithmeticmeancurve/

.. image:: ../examplecurves-icon.svg
   :height: 150px
   :width: 150px
   :alt: An E of 3 lines.
   :align: center

.. warning::

   This module is in an alpha development state. With future releases the wording
   (function, attribute and class names) may change towards a more common understanding.
   Additional mean curve calculation algorithms will be added, which might replace the
   current default calculation.

   Current main construction parts are the documentation, docstrings and additional
   tests of this package.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api_reference/index.rst

Installation
============

.. code-block:: shell

   $ pip install examplecurves

Basic Usage
===========

Using :func:`examplecurves.create` is the default way to get example curves.
The necessary argument is the *family_name* of the family of curves, which are listed
in the api-reference of this documentation.

.. plot::
   :include-source:

    import examplecurves
    requested_curves = examplecurves.Static.create("nonlinear0")
    examplecurves.plot_curves(requested_curves)

It is possible to make a selection of the returned curves by the curves indexes.
By *curve_selection* a list of indexes defines the curves to be returned only.

.. plot::
   :include-source:

    import examplecurves
    requested_curves = examplecurves.Static.create("nonlinear0", curve_selection=[0,2,4])
    examplecurves.plot_curves(requested_curves)

Cutting of curves is also possible by either defining the index (integer position
within a sequence) or list of maximum 3 entries defining a slice. [None, -3] would lead
to slicing the curves like `curve[:-3]. The default behavior of providing an integer
only is equivalent to `curve[:i]`.

.. plot::
   :include-source:

    import examplecurves
    requested_curves = examplecurves.Static.create(
       family_name="nonlinear0",
       cut_curves_at=3,
       curve_selection=[0,2,4]
    )
    examplecurves.plot_curves(requested_curves)

The requested curves can be offset by an iterable of custom offsets.

.. plot::
   :include-source:

    import examplecurves
    requested_curves = examplecurves.Static.create(
       family_name="nonlinear0",
       cut_curves_at=3,
       offsets=[(1, 2), (3, 4), (5, 6)],
       curve_selection=[0,2,4]
    )
    examplecurves.plot_curves(requested_curves)

The examplecurves might come with predefined offsets, which can be invoked by
*predefined_offset* defining the index of the offset. *predefined_offset* overrules
*offsets*.

.. plot::
   :include-source:

    import examplecurves
    requested_curves = examplecurves.Static.create(
       family_name="nonlinear0",
       cut_curves_at=3,
       offsets=[(1, 2), (3, 4), (5, 6)],
       predefined_offset=1,
       curve_selection=[0,2,4]
    )
    examplecurves.plot_curves(requested_curves)


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
