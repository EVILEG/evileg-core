# -*- coding: utf-8 -*-

from django.urls import path

from .views import EMarkdownView

app_name = 'evileg_core'
urlpatterns = [
    path('markdown/', EMarkdownView.as_view(), name='markdown')
]
