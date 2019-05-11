===============
Getting started
===============

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
