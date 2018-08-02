# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.utils.translation import ugettext_lazy as _

from .widgets import ELesserAdminDateWidget


class EDateRangeForm(forms.Form):
    """
    Form with range input of dates. This form is using in Django administration panel
    """
    class Media:
        js = (
            static("admin/js/calendar.js"),
            static("admin/js/admin/DateTimeShortcuts.js"),
        )
        css = {
            'all': (static("admin/css/widgets.css"),)
        }

    def __init__(self, request, *args, **kwargs):
        """
        Constructor. In this constructor we initialize fields for date range filter
        """
        field_name = kwargs.pop('field_name')
        super().__init__(*args, **kwargs)

        self.fields['%s__gte' % field_name] = forms.DateField(
            label='',
            widget=ELesserAdminDateWidget(attrs={'placeholder': _('From date')}),
            localize=True,
            required=False
        )

        self.fields['%s__lte' % field_name] = forms.DateField(
            label='',
            widget=ELesserAdminDateWidget(attrs={'placeholder': _('To date')}),
            localize=True,
            required=False,
        )
