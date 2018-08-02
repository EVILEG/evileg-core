.. evileg_core documentation master file, created by
   sphinx-quickstart on Thu Aug  2 18:48:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================================
(ESNF-C) EVILEG Social Network Framework - Core Module
======================================================

`Social network EVILEG <https://evileg.com/>`_. Django app - core module

This application is core module of EVILEG Social network

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Quick start
===========

1. Add "evileg_core" to your INSTALLED_APPS setting like this

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'evileg_core',
    ]

2. Create your first moderated model

.. code-block:: python

   class Post(EAbstractModeratedPost):
      pass

3. Make migrations

.. code-block:: bash

   python manage.py makemigrations

4. Migrate

.. code-block:: bash

   python manage.py migrate

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
