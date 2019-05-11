========
Backends
========

evileg\_core.backends module
----------------------------

.. automodule:: evileg_core.backends
    :members:
    :undoc-members:
    :show-inheritance:

Examples
--------

EEmailOrUsernameModelBackend
````````````````````````````

Added authentication backend to your settings.py

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'evileg_core.backends.EEmailOrUsernameModelBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

And authenticate yourself using email instead of username
