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
    """
    Markdown widget for rendering in the templates
    """

    def __init__(self, attrs=None, documentation_link=None, placeholder=None, upload_link=None, upload_file_link=None,
                 extended_mode=True, fullscreen=True):
        self.documentation_link = documentation_link
        self.placeholder = placeholder
        self.upload_link = upload_link
        self.upload_file_link = upload_file_link
        self.codemirror_theme = 'idea'
        self.markdown_codemirror_theme = 'markdown_idea'
        self.extended_mode = extended_mode
        self.fullscreen = fullscreen
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        return render_to_string(
            template_name='evileg_core/markdown_widget.html',
            context={
                'widget_id': attrs['id'],
                'documentation_link': self.documentation_link,
                'placeholer': self.placeholder,
                'upload_link': self.upload_link,
                'upload_file_link': self.upload_file_link,
                'final_attrs': flatatt(self.build_attrs(self.attrs, attrs, name=name)),
                'text': force_text(value or ''),
                'codemirror_theme': self.codemirror_theme,
                'markdown_codemirror_theme': self.markdown_codemirror_theme,
                'extended_mode': self.extended_mode,
                'fullscreen': self.fullscreen
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
