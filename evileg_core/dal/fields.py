# -*- coding: utf-8 -*-

from dal import autocomplete
from django import forms
from django.db import models
from django.urls import reverse_lazy
from tagging.fields import TagField, TagFormField


class ETagFormField(TagFormField):

    def __init__(self, autocomplete_pattern, *args, **kwargs):
        if not autocomplete_pattern:
            raise ValueError('This parameter is mandatory')
        kwargs.update({'widget': autocomplete.TaggingSelect2(url=reverse_lazy(autocomplete_pattern))})
        super().__init__(*args, **kwargs)


class ETagField(TagField):

    def __init__(self, *args, **kwargs):
        self.autocomplete_pattern = kwargs.pop('autocomplete_pattern', '')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({'form_class': ETagFormField})
        return super().formfield(autocomplete_pattern=self.autocomplete_pattern, **kwargs)


class EForeignKeyFormField(forms.ModelChoiceField):

    def __init__(self, autocomplete_pattern, *args, **kwargs):
        if not autocomplete_pattern:
            raise ValueError('This parameter is mandatory')
        kwargs.update({'widget': autocomplete.ModelSelect2(url=reverse_lazy(autocomplete_pattern))})
        super().__init__(*args, **kwargs)


class EForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        self.autocomplete_pattern = kwargs.pop('autocomplete_pattern', '')
        super().__init__(*args, **kwargs)

    def formfield(self, *, using=None, **kwargs):
        kwargs.update({'form_class': EForeignKeyFormField})
        return super().formfield(autocomplete_pattern=self.autocomplete_pattern, using=using, **kwargs)


class EModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def __init__(self, autocomplete_pattern, *args, **kwargs):
        if not autocomplete_pattern:
            raise ValueError('This parameter is mandatory')
        kwargs.update({'widget': autocomplete.ModelSelect2Multiple(url=reverse_lazy(autocomplete_pattern))})
        super().__init__(*args, **kwargs)


class EManyToManyField(models.ManyToManyField):

    def __init__(self, *args, **kwargs):
        self.autocomplete_pattern = kwargs.pop('autocomplete_pattern', '')
        super().__init__(*args, **kwargs)

    def formfield(self, *, using=None, **kwargs):
        kwargs.update({'form_class': EModelMultipleChoiceField})
        return super().formfield(autocomplete_pattern=self.autocomplete_pattern, using=using, **kwargs)
