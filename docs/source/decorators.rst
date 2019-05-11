==========
Decorators
==========

evileg\_core.decorators module
------------------------------

.. automodule:: evileg_core.decorators
    :members:
    :undoc-members:
    :show-inheritance:


Examples
--------

Using recaptcha
```````````````

1. Add recaptcha key to settings.py

.. code-block:: python

    GOOGLE_RECAPTCHA_SECRET_KEY = 'your-secret-token'
    GOOGLE_RECAPTCHA_SITE_KEY = 'your-site-key'

2. Add recaptcha to view in urls

.. code-block:: python

    from django.conf.urls import url
    from evileg_core.decorators import recaptcha

    from . import views

    app_name = 'registration'
    urlpatterns = [
        url(r'^register/$', recaptcha(views.RegisterView.as_view()), name='register'),
    ]

2. Add recaptcha site key in template with form

.. code-block:: html

    <form action="{% url 'register' %}" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        {% load evileg_core %}
        {% recaptcha %}
        {% if messages %}
            {% for message in messages %}
                {{ message }}
            {% endfor %}
        {% endif %}
        <input type="submit" value="Register">
    </form>

3. Check recaptcha in your form view

.. code-block:: python

    class RegisterView(FormView):
        form_class = UserCreationForm
        template_name = 'register.html'

        def form_valid(self, form):
            if self.request.recaptcha_is_valid:
                form.save()
                return render(self.request, 'register_success.html', self.get_context_data())
            return render(self.request, 'register.html', self.get_context_data())
