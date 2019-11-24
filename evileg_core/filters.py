# -*- coding: utf-8 -*-

import datetime

import django_filters
from django.contrib import admin
from django.contrib.admin.filters import FieldListFilter
from django.db.models import DateField, Q
from django.utils.translation import ugettext_lazy as _
from django_filters import filters

from .forms import EDateRangeForm


class EDateRangeFilter(FieldListFilter):
    """
    Date range filter for Django administration panel

    :param template: html template for filter rendering
    """
    template = 'evileg_core/date_range_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super().__init__(field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, changelist):
        changelist.params.pop(self.lookup_kwarg_since, None)
        changelist.params.pop(self.lookup_kwarg_upto, None)
        return ({'get_query': changelist.params,},)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        """

        :param request: HTTP request with filter parameters
        :return: EDateRangeForm
        """
        return EDateRangeForm(request, data=self.used_parameters, field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            filter_params = dict(filter(lambda x: bool(x[1]), self.form.cleaned_data.items()))
            if filter_params.get(self.lookup_kwarg_upto) is not None:
                value = filter_params.pop(self.lookup_kwarg_upto)
                filter_params['%s__lt' % self.field_path] = value + datetime.timedelta(days=1)

            return queryset.filter(**filter_params)
        else:
            return queryset


FieldListFilter.register(lambda f: isinstance(f, DateField), EDateRangeFilter)


class ENotNullFilter(admin.SimpleListFilter):
    """
    Filter by null fields, for example for Foreign Key

    :param title: Title of filter
    :param parameter_name: Field name
    """
    title = _('Filter title not set')
    parameter_name = 'parameter name not set'

    def lookups(self, request, model_admin):
        return (
            ('not_null', _('Not empty only')),
            ('null', _('Empty only')),
        )

    def queryset(self, request, queryset):
        filter_string = self.parameter_name + '__isnull'
        if self.value() == 'not_null':
            is_null_false = {filter_string: False}
            return queryset.filter(**is_null_false)

        if self.value() == 'null':
            is_null_true = {filter_string: True}
            return queryset.filter(**is_null_true)


class EExactEmptyFilter(admin.SimpleListFilter):
    """
    Filter by empty fields, for example for CharField or Url

    :param title: Title of filter
    :param parameter_name: Field name
    """
    title = _('Filter title not set')
    parameter_name = 'parameter name not set'

    def lookups(self, request, model_admin):
        return (
            ('not_null', _('Not empty only')),
            ('null', _('Empty only')),
        )

    def queryset(self, request, queryset):
        filter_string = self.parameter_name + '__exact'
        if self.value() == 'not_null':
            is_null_false = {filter_string: ''}
            return queryset.filter(~Q(**is_null_false))

        if self.value() == 'null':
            is_null_true = {filter_string: ''}
            return queryset.filter(Q(**is_null_true))


class EFilterBase(django_filters.FilterSet):
    advanced_search = False

    search = filters.CharFilter(field_name='search', method='main_search')

    class Meta:
        fields = ['search']

    def main_search(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(content__icontains=value))

    @classmethod
    def create(cls, target_model):
        class FilterBase(EFilterBase):
            class Meta(EFilterBase.Meta):
                model = target_model
        return FilterBase


class EArticleFilter(EFilterBase):
    advanced_search = True

    ordering_by_title = filters.OrderingFilter(choices=(
        ('title', _('Title')),
        ('-title', _('Title (descending)')),
    ), label=_('Sort by title'))
    ordering_by_views = filters.OrderingFilter(choices=(
        ('-views', _('Views')),
        ('views', _('Views (descending)'))
    ), label=_('Sort by views'))
    ordering_by_pub_date = filters.OrderingFilter(choices=(
        ('pub_date', _('Publication date')),
        ('-pub_date', _('Publication date (descending)')),
    ), label=_('Sort by publication date'))

    @classmethod
    def create(cls, target_model):
        class ArticleFilter(EArticleFilter):
            class Meta(EArticleFilter.Meta):
                model = target_model
        return ArticleFilter


class ESectionFilter(EFilterBase):
    advanced_search = True

    ordering_by_title = filters.OrderingFilter(choices=(
        ('title', _('Title')),
        ('-title', _('Title (descending)')),
    ), label=_('Sort by title'))

    @classmethod
    def create(cls, target_model):
        class SectionFilter(ESectionFilter):
            class Meta(ESectionFilter.Meta):
                model = target_model
        return SectionFilter
