# -*- coding: utf-8 -*-

from django.core.cache import cache


def invalidate_model_cached_property(model_object, function):
    """
    Function for invalidation model cached property

    :param model_object: model instance, on which should be invalidated property
    :param function: wrapped function, which should be invalidated
    :return:
    """
    cache_keys = cache.keys('evileg_core_model_cached_property_{}_{}_{}_*'.format(
        model_object._meta.db_table,
        model_object.id,
        function.__name__,
    ))
    for key in cache_keys:
        cache.delete(key)
