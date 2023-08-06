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
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/sonicvision/badge/?style=flat
    :target: https://readthedocs.org/projects/sonicvision
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/sonicvision/sonicvision.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sonicvision/sonicvision

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/sonicvision/sonicvision?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/sonicvision/sonicvision

.. |requires| image:: https://requires.io/github/sonicvision/sonicvision/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/sonicvision/sonicvision/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/sonicvision/sonicvision/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/sonicvision/sonicvision

.. |codecov| image:: https://codecov.io/gh/sonicvision/sonicvision/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sonicvision/sonicvision

.. |landscape| image:: https://landscape.io/github/sonicvision/sonicvision/master/landscape.svg?style=flat
    :target: https://landscape.io/github/sonicvision/sonicvision/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/grade/[Get ID from https://app.codacy.com/app/sonicvision/sonicvision/settings].svg
    :target: https://www.codacy.com/app/sonicvision/sonicvision
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/sonicvision/sonicvision/badges/gpa.svg
   :target: https://codeclimate.com/github/sonicvision/sonicvision
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/sonicvision.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sonicvision

.. |wheel| image:: https://img.shields.io/pypi/wheel/sonicvision.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/sonicvision

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sonicvision.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sonicvision

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sonicvision.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/sonicvision

.. |commits-since| image:: https://img.shields.io/github/commits-since/sonicvision/sonicvision/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/sonicvision/sonicvision/compare/v0.0.1...master


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/sonicvision/sonicvision/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/sonicvision/sonicvision/


.. end-badges

Quick Prototyping for deep learning based vision tasks

* Free software: Apache Software License 2.0

Installation
============

::

    pip install sonicvision

You can also install the in-development version with::

    pip install https://github.com/sonicvision/sonicvision/archive/master.zip


Documentation
=============


https://sonicvision.readthedocs.io/


Development
===========

To run all the tests run::

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
