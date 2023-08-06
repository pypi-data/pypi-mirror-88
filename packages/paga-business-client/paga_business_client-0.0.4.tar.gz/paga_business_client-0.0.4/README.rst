========
Overview
========

Paga Business CLient

* Free software: MIT license

Installation
============

::

    pip install paga_business_client

You can also install the in-development version with::

    pip install git+ssh://git@github.com/pagadevcomm/pagadevcomm/paga_business_library.git@master

Documentation
=============


To use the project:

.. code-block:: python

    import paga_business_client
    paga_business_client.longest()


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
