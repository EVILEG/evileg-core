=====
Admin
=====

evileg\_core.admin module
-------------------------

.. automodule:: evileg_core.admin
    :members:
    :undoc-members:
    :show-inheritance:

Examples
--------

Using of EPostModeratedAdmin for Post Model, which inherits from EAbstractModeratedPost.

.. code-block:: python

    from django.contrib import admin
    from evileg_core.admin import EPostModeratedAdmin

    from your_app.models import Post

    admin.site.register(Post, EPostModeratedAdmin)

