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


class EPostForm(forms.ModelForm):
    """
    Form class for class, which inherits from evileg_core.models.EAbstractPost.
    User (author) of post should be sent to constructor.
    """
    class Meta:
        fields = ['content_markdown']

    def __init__(self, user=None, *args, **kwargs):
        if not user:
            raise ValueError('This parameter is mandatory')
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class EArticleForm(EPostForm):
    """
    Form class for class, which inherits from evileg_core.models.EAbstractArticle.
    In this form added title field.
    """
    class Meta:
        fields = ['title'] + EPostForm.Meta.fields


class ESectionForm(EArticleForm):
    """
    Form class for class, which inherits from evileg_core.models.EAbstractSection.
    """
    pass
