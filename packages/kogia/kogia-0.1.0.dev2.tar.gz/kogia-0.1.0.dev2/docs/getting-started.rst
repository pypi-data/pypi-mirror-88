===============
Getting started
===============

Kogia is free and open-source software, distributed under
the `Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.
Being a reusable Django application, you will need to install Python and
Django before you can use it.

.. contents::
   :local:
   :depth: 2


----


Requirements
============

Python and Django compatibility
-------------------------------

This project requires the following:

======= ===================================
Django  Python
======= ===================================
2.2 LTS 3.5, 3.6, 3.7, 3.8 (added in 2.2.8)
------- -----------------------------------
3.1     3.6, 3.7, 3.8
======= ===================================

We highly recommend the latest release of each series for both Python and
Django.


Python virtual environment
--------------------------

It is highly recommended to install Django, Kogia, and all other Python
dependencies of your project within
a `Python virtual environment <https://docs.python.org/3/library/venv.html>`_.


----


Install Kogia
=================

Get the latest release from PyPI
--------------------------------

This project is released on `PyPI <https://pypi.org/project/kogia/>`_,
the Python Package Index. You can install the latest release with pip:

.. code-block:: bash

    pip install kogia


Get the latest development version
----------------------------------

.. note::

   This option is not recommended unless you want to try incoming changes. You might
   encounter new bugs in the development version.

You can install the latest development version of this project from
the `Git repository <https://gitlab.com/pascalpepe/kogia>`_:

.. code-block:: bash

    pip install git+https://gitlab.com/pascalpepe/kogia.git@main#egg=kogia


----


Quick start guide
=================

Settings
--------

Update your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'kogia.core',
        'kogia.intl',
        'kogia.pages',
    ]
