# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def activities_count(activity_set, model_name):
    if model_name:
        return activity_set.search(model=ContentType.objects.get(model=model_name).model_class()).count()
    return activity_set.count()
