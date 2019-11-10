========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires| |coveralls|
        | |scrutinizer| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-locked_dict/badge/?style=flat
    :target: https://readthedocs.org/projects/python-locked-dict/
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/sthagen/python-locked_dict.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sthagen/python-locked_dict

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/sthagen/python-locked_dict?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/sthagen/python-locked_dict

.. |requires| image:: https://requires.io/github/sthagen/python-locked_dict/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/sthagen/python-locked_dict/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/sthagen/python-locked_dict/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/sthagen/python-locked_dict

.. |codecov| image:: https://codecov.io/github/sthagen/python-locked_dict/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sthagen/python-locked_dict

.. |codeclimate| image:: https://codeclimate.com/github/sthagen/python-locked_dict/badges/gpa.svg
   :target: https://codeclimate.com/github/sthagen/python-locked_dict
   :alt: CodeClimate Quality Status

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

Dict to allow context managed thread safe and mutable iterations through a lock.

* Free software: MIT license

Installation
============

::

    pip install locked-dict

Documentation
=============

https://python-locked-dict.readthedocs.io/en/latest/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

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
