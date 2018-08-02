# -*- coding: utf-8 -*-

import datetime

from django.contrib.admin.filters import FieldListFilter
from django.db.models import DateField

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
