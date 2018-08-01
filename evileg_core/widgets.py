# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget


class ELesserAdminDateWidget(AdminDateWidget):
    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = [
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
        ]
        return forms.Media(js=["admin/js/%s" % path for path in js])