# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext_lazy as _


def recaptcha(function):
    """
    Google recaptcha decorator. It can be used against robots and brute force.


    :param function: wrapped view function, which should be checked via Google recaptcha
    :return: wrapped function
    """
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        google_recaptcha_secret_key = getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', None)
        if not google_recaptcha_secret_key or len(google_recaptcha_secret_key) == 0:
            request.recaptcha_is_valid = True
            return function(request, *args, **kwargs)

        if request.user.is_authenticated:
            request.recaptcha_is_valid = True
            return function(request, *args, **kwargs)

        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': google_recaptcha_secret_key,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, _('Invalid reCAPTCHA. Please try again.'))
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def non_login_required(function=None, redirect_url='/'):
    """
    Decorator for views that checks that the user is not logged in, redirecting
    to the main page or target page by redirect_url if user is logged in.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
