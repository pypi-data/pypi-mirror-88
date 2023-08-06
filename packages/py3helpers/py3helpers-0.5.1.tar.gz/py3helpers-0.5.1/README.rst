========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/py3helpers/badge/?style=flat
    :target: https://readthedocs.org/projects/py3helpers
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/adbailey4/py3helpers.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/adbailey4/py3helpers

.. |requires| image:: https://requires.io/github/adbailey4/py3helpers/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/adbailey4/py3helpers/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/adbailey4/py3helpers/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/adbailey4/py3helpers

.. |version| image:: https://img.shields.io/pypi/v/py3helpers.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/py3helpers

.. |wheel| image:: https://img.shields.io/pypi/wheel/py3helpers.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/py3helpers

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py3helpers.svg
    :alt: Supported versions
    :target: https://pypi.org/project/py3helpers

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py3helpers.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/py3helpers

.. |commits-since| image:: https://img.shields.io/github/commits-since/adbailey4/py3helpers/v0.5.1.svg
    :alt: Commits since latest release
    :target: https://github.com/adbailey4/py3helpers/compare/v0.5.1...master



.. end-badges

General python functions and classes which could be used across multiple projects.

* Free software: BSD 3-Clause License

Installation
============
::

    pip install py3helpers

You can also install the in-development version with::

    pip install https://github.com/adbailey4/py3helpers/archive/master.zip

You to allow access to seq_tools, you need to install with::

    pip install py3helpers[seq_tools]

Or you can install from source with::

    git clone https://github.com/adbailey4/python_utils
    cd python_utils
    pip install -e.[seq_tools]
    python setup.py test


Documentation
=============


https://py3helpers.readthedocs.io/


Development
===========

To run the all tests run::

    tox

