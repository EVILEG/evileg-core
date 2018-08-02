# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget


class ELesserAdminDateWidget(AdminDateWidget):
    """
    ELesserAdminDateWidget is using for filters in admin panels.
    From media of this class were removed some js files because it invoked reinitialization of fields.
    This field is using in Django administration panel
    """
    @property
    def media(self):
        """
        Method will return needed js files for this field

        :return: django.forms.Media
        """
        extra = '' if settings.DEBUG else '.min'
        js = [
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
        ]
        return forms.Media(js=["admin/js/%s" % path for path in js])