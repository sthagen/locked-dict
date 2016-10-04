========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-locked_dict/badge/?style=flat
    :target: https://readthedocs.org/projects/python-locked_dict
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/sdrees/python-locked_dict.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sdrees/python-locked_dict

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/sdrees/python-locked_dict?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/sdrees/python-locked_dict

.. |requires| image:: https://requires.io/github/sdrees/python-locked_dict/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/sdrees/python-locked_dict/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/sdrees/python-locked_dict/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/sdrees/python-locked_dict

.. |codecov| image:: https://codecov.io/github/sdrees/python-locked_dict/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sdrees/python-locked_dict

.. |landscape| image:: https://landscape.io/github/sdrees/python-locked_dict/master/landscape.svg?style=flat
    :target: https://landscape.io/github/sdrees/python-locked_dict/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/sdrees/python-locked_dict
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/sdrees/python-locked_dict/badges/gpa.svg
   :target: https://codeclimate.com/github/sdrees/python-locked_dict
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/locked-dict.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/locked-dict

.. |downloads| image:: https://img.shields.io/pypi/dm/locked-dict.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/locked-dict

.. |wheel| image:: https://img.shields.io/pypi/wheel/locked-dict.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/locked-dict

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/locked-dict.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/locked-dict

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/locked-dict.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/locked-dict


.. end-badges

Dict to allow context managed thread safe and mutable iterations through a lock.

* Free software: BSD license

Installation
============

::

    pip install locked-dict

Documentation
=============

https://python-locked_dict.readthedocs.io/

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
