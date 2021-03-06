# -*- coding: utf-8 -*-

from django.apps import apps
from django.urls import path

from .views import EMarkdownView

app_name = 'evileg_core'
urlpatterns = [
    path('markdown/', EMarkdownView.as_view(), name='markdown')
]

if apps.is_installed('dal') and apps.is_installed('dal_select2') and apps.is_installed('tagging'):

    from django.contrib.auth.decorators import login_required
    from tagging.models import Tag
    from .dal.views import EGenericAutocomplete

    urlpatterns.append(path(
        'autocomplete-tags/',
        login_required(EGenericAutocomplete.as_view(
            queryset=Tag.objects.all(),
            fields=['name__istartswith']
        )),
        name='autocomplete_tag')
    )
