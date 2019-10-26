# -*- coding: utf-8 -*-

from functools import wraps, partial

from django.conf import settings
from django.core.cache import cache


def model_cached_property(method=None, timeout=getattr(settings, "MODEL_CACHED_PROPERTY_TIMEOUT", 60)):
    """
    Decorator for caching expensive properties in django models

    WARNING:
    This decorator doesn`t work with dynamic objects in function arguments,ghgyyy
    For example it doesn`t work with AnonymousUser, only with authenticated Useryhhh

    :param timeout: cache timeout
    :param method: wrapped method, which should be cached
    :return: wrapped function
    """
    if method is None:
        return partial(model_cached_property, timeout=timeout)

    @wraps(method)
    def function_wrapper(model_object, *args, **kwargs):
        cache_key = 'evileg_core_model_cached_property_{}_{}_{}_{}_'.format(
            model_object._meta.db_table, model_object.id, method.__name__,
            "{} {}".format(args, kwargs).replace(" ", "_")
        )
        result = cache.get(cache_key)
        if result is not None:
            return result
        result = method(model_object, *args, **kwargs)
        cache.set(cache_key, result, timeout=timeout)
        return result

    return function_wrapper
