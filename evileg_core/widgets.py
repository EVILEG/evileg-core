# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.encoding import force_text


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


class EMarkdownWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        return render_to_string(
            template_name='evileg_core/markdown_widget.html',
            context={
                'widget_id': attrs['id'],
                'final_attrs': flatatt(self.build_attrs(self.attrs, attrs, name=name)),
                'text': force_text(value or '')
            }
        )

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs
