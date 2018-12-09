# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

register = template.Library()


CLASSIC = 1
DARCULA = 2

STYLE_CHOICES = (
    (CLASSIC, _('Classic')),
    (DARCULA, _('Darcula'))
)

THEMES_CSS = {
    CLASSIC: 'css/evileg_core.css',
    DARCULA: 'css/evileg_core_darcula.css'
}

THEMES_CSS_MIN = {
    CLASSIC: 'css/evileg_core.min.css',
    DARCULA: 'css/evileg_core_darcula.min.css'
}


@register.simple_tag
def get_theme(theme):
    return static(THEMES_CSS[theme])


@register.simple_tag
def get_theme_min(theme):
    return static(THEMES_CSS_MIN[theme])


@register.filter
def activities_count(activity_set, model_name):
    if model_name:
        return activity_set.search(model=ContentType.objects.get(model=model_name).model_class()).count()
    return activity_set.count()


@register.simple_tag
def evileg_core_css():
    return static("css/evileg_core.css")


@register.simple_tag
def evileg_core_min_css():
    return static("css/evileg_core.min.css")


@register.simple_tag
def evileg_core_icons_css():
    return static("css/materialdesignicons.css")


@register.simple_tag
def evileg_core_icons_min_css():
    return static("css/materialdesignicons.min.css")


@register.simple_tag
def evileg_core_js():
    return static("js/evileg_core.js")


@register.simple_tag
def evileg_core_min_js():
    return static("js/evileg_core.min.js")


@register.simple_tag
def evileg_core_popper_min_js():
    return static("js/popper.min.js")


@register.simple_tag
def evileg_core_jquery_min_js():
    return static("js/jquery-3.3.1.min.js")


@register.simple_tag
def evileg_core_markdown_js():
    return static("js/markdown.js")


@register.simple_tag
def evileg_core_markdown_min_js():
    return static("js/markdown.min.js")


@register.inclusion_tag('evileg_core/partials/object_list_preview.html', takes_context=True)
def object_list_preview(context):
    return context
