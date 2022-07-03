========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-locked_dict/badge/?style=flat
    :target: https://readthedocs.org/projects/python-locked-dict/
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/locked-dict.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/locked-dict/

.. |downloads| image:: https://img.shields.io/pypi/dm/locked-dict.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.org/project/locked-dict/

.. |wheel| image:: https://img.shields.io/pypi/wheel/locked-dict.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.org/project/locked-dict/

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/locked-dict.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.org/project/locked-dict/

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/locked-dict.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.org/project/locked-dict/

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/sthagen/python-locked_dict/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/sthagen/python-locked_dict/


.. end-badges

Implementation of dict supporting context managed thread safe and mutable iterations through a lock.

* Free software: MIT license

Installation
============

::

    pipx install locked-dict

or::

    python -m pip install locked-dict

Documentation
=============

https://python-locked-dict.readthedocs.io/en/latest/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from the different tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

**Note**: The name of the default branch is `default`.
