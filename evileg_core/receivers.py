# -*- coding: utf-8 -*-


def cache_invalidate_activity(sender, instance, **kwargs):
    instance.invalidate_cache()
