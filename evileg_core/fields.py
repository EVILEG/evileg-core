# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from .utils import EMarkdownWorker
from .widgets import EMarkdownWidget


class EMarkdownField(models.TextField):
    """
    This field save markdown text with auto-populate text to html field.
    This field must be used with second text field for html content.
    This field support django-modeltranslation package.

    EMarkdownField can use upload_link and upload_file_link for invoke upload dialog from backend.
    Unfortunately, this mechanism is not fully developed for using like 3d party.
    We develop this in near future.
    """

    def set_markdown(self, instance=None, **kwargs):
        value = getattr(instance, self.attname)
        if value and len(value) > 0:
            languages = getattr(settings, "LANGUAGES", None)
            if 'modeltranslation' in settings.INSTALLED_APPS and self.name.endswith(
                    tuple([code for code, language in languages])):
                instance.__dict__['{}_{}'.format(self.html_field, self.name[-2:])] = EMarkdownWorker(
                    value).get_text()
            else:
                instance.__dict__[self.html_field] = EMarkdownWorker(value).get_text()

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        pre_save.connect(self.set_markdown, sender=cls)

    def __init__(self, html_field=None, *args, **kwargs):
        self.html_field = html_field
        self.placeholder = kwargs.pop("placeholder", '')
        self.upload_link = kwargs.pop("upload_link", None)
        self.upload_file_link = kwargs.pop("upload_file_link", None)
        self.extended_mode = kwargs.pop("extended_mode", True)
        self.fullscreen = kwargs.pop("fullscreen", True)
        if not self.upload_link:
            self.upload_link = getattr(settings, 'MARKDOWN_UPLOAD_LINK', None)
        if not self.upload_file_link:
            self.upload_file_link = getattr(settings, "MARKDOWN_UPLOAD_FILE_LINK", None)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self._get_form_class(),
            'documentation_link': getattr(settings, "MARKDOWN_DOCUMENTATION_LINK", None),
            'placeholder': self.placeholder,
            'upload_link': self.upload_link,
            'upload_file_link': self.upload_file_link,
            'extended_mode': self.extended_mode,
            'fullscreen': self.fullscreen
        }
        defaults.update(**kwargs)
        return super().formfield(**defaults)

    @staticmethod
    def _get_form_class():
        return EMarkdownFormField


class EMarkdownFormField(forms.fields.CharField):
    """
    EMarkdownFormField using in django forms
    """
    def __init__(self, documentation_link=None, placeholder=None, upload_link=None, upload_file_link=None,
                 extended_mode=True, fullscreen=True, *args, **kwargs):
        kwargs.update({'widget': EMarkdownWidget(
            documentation_link=documentation_link,
            placeholder=placeholder,
            upload_link=upload_link,
            upload_file_link=upload_file_link,
            extended_mode=extended_mode,
            fullscreen=fullscreen
        )})
        super().__init__(*args, **kwargs)
