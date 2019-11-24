# -*- coding: utf-8 -*-

import random

from bootstrap4.utils import add_css_class
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

register = template.Library()


STATIC_CONTENT_VERSION = 54

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

THEMES_CSS_CDN = {
    CLASSIC: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/css/evileg_core.css',
    DARCULA: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/css/evileg_core_darcula.css'
}

THEMES_CSS_MIN_CDN = {
    CLASSIC: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/css/evileg_core.min.css',
    DARCULA: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/css/evileg_core_darcula.min.css'
}

GRADIENTS = (
    'aqua-gradient',
    'clear-sky-gradient',
    'passion-gradient',
    'timber-gradient',
    'night-and-day-gradient',
    'sage-percuasion-gradient',
    'lizard-gradient',
    'piglet-gradient',
    'dark-knight-gradient',
    'curiosity-blue-gradient',
    'virgin-amerika-gradient',
    'vine-gradient'
)


@register.simple_tag
def random_gradient():
    return random.choice(GRADIENTS)


COMMON = 1
COMMON_MIN = 2
CDN = 3
CDN_MIN = 4

EVILEG_CORE_JS_STATIC_FILES = {
    COMMON: 'js/evileg_core.js',
    COMMON_MIN: 'js/evileg_core.min.js',
    CDN: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/js/evileg_core.js',
    CDN_MIN: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/js/evileg_core.min.js'
}

POPPER_JS_STATIC_FILES = {
    COMMON_MIN: 'js/popper.min.js',
    CDN_MIN: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/js/popper.min.js'
}


JQUERY_JS_STATIC_FILES = {
    COMMON_MIN: 'js/jquery-3.3.1.min.js',
    CDN_MIN: 'https://cdn.jsdelivr.net/gh/EVILEG/evileg-core@master/evileg_core/static/js/jquery-3.3.1.min.js'
}


def select_static_minified_file(cdn, files_dict):
    if cdn:
        file_url = files_dict[CDN_MIN]
    else:
        file_url = static(files_dict[COMMON_MIN])
    return '{}?{}'.format(file_url, STATIC_CONTENT_VERSION)


def select_static_file(cdn, minified, files_dict):
    if cdn and minified:
        file_url = files_dict[CDN_MIN]
    elif cdn:
        file_url = files_dict[CDN]
    elif minified:
        file_url = static(files_dict[COMMON_MIN])
    else:
        file_url = static(files_dict[COMMON])
    return '{}?{}'.format(file_url, STATIC_CONTENT_VERSION)


@register.simple_tag(takes_context=True)
def render_template_full(context, obj):
    if obj:
        return obj.render_template_full(context)
    return ''


@register.simple_tag(takes_context=True)
def render_template_preview(context, obj):
    if obj:
        return obj.render_template_preview(context)
    return ''


@register.simple_tag(takes_context=True)
def render_template_info(context, obj):
    if obj:
        return obj.render_template_info(context)
    return ''


@register.simple_tag
def render_template_mail(obj):
    if obj:
        return obj.render_template_mail()
    return ''


@register.filter
def activities_count(activity_set, model_name):
    if model_name:
        return activity_set.search(model=ContentType.objects.get(model=model_name).model_class()).count()
    return activity_set.count()


@register.simple_tag
def evileg_core_css(theme=CLASSIC,
                    minified=getattr(settings, "EVILEG_CORE_MIN_STATIC_FILES", True),
                    cdn=getattr(settings, "EVILEG_CORE_CDN", False)):
    if cdn and minified:
        file_url = THEMES_CSS_MIN_CDN[theme]
    elif cdn:
        file_url = THEMES_CSS_CDN[theme]
    elif minified:
        file_url = static(THEMES_CSS_MIN[theme])
    else:
        file_url = static(THEMES_CSS[theme])
    return '{}?{}'.format(file_url, STATIC_CONTENT_VERSION)


@register.simple_tag
def evileg_core_icons_css():
    return static("css/materialdesignicons.css")


@register.simple_tag
def evileg_core_icons_min_css():
    return static("css/materialdesignicons.min.css")


@register.simple_tag
def evileg_core_cropper_css():
    return static("css/cropper.css")


@register.simple_tag
def evileg_core_cropper_min_css():
    return static("css/cropper.min.css")


@register.simple_tag
def evileg_core_js(minified=getattr(settings, "EVILEG_CORE_MIN_STATIC_FILES", True),
                   cdn=getattr(settings, "EVILEG_CORE_CDN", False)):
    return select_static_file(cdn=cdn, minified=minified, files_dict=EVILEG_CORE_JS_STATIC_FILES)


@register.simple_tag
def evileg_core_popper_js(cdn=getattr(settings, "EVILEG_CORE_CDN", False)):
    return select_static_minified_file(cdn=cdn, files_dict=POPPER_JS_STATIC_FILES)


@register.simple_tag
def evileg_core_jquery_js(cdn=getattr(settings, "EVILEG_CORE_CDN", False)):
    return select_static_minified_file(cdn=cdn, files_dict=JQUERY_JS_STATIC_FILES)


@register.simple_tag
def evileg_core_markdown_js():
    return static("js/markdown.js")


@register.simple_tag
def evileg_core_markdown_min_js():
    return static("js/markdown.min.js")


@register.simple_tag
def evileg_core_cropper_js():
    return static("js/cropper.js")


@register.simple_tag
def evileg_core_cropper_min_js():
    return static("js/cropper.min.js")


@register.inclusion_tag('evileg_core/partials/object_list_preview.html', takes_context=True)
def object_list_preview(context):
    return context


@register.inclusion_tag('evileg_core/recaptcha.html')
def recaptcha(classes=''):
    """
    Google recaptcha template tag, which should be included in forms

    :param classes: additional classes
    :return: rendered template
    """
    return {
        'classes': add_css_class('g-recaptcha', classes, prepend=True),
        'site_key': getattr(settings, "GOOGLE_RECAPTCHA_SITE_KEY", ''),
    }


@register.simple_tag
def breadcrumb_schema():
    return "http://schema.org/BreadcrumbList"


@register.inclusion_tag('evileg_core/breadcrumb_home.html')
def breadcrumb_home(url='/', title=''):
    return {'url': url, 'title': title}


@register.inclusion_tag('evileg_core/breadcrumb_item.html')
def breadcrumb_item(url, title, position):
    return {'url': url, 'title': title, 'position': position}


@register.inclusion_tag('evileg_core/breadcrumb_active.html')
def breadcrumb_active(url, title, position):
    return {'url': url, 'title': title, 'position': position}


@register.filter
def human_format(num, round_to=1):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{}{}'.format(
        '{:.{}f}'.format(round(num, round_to), round_to).rstrip('0').rstrip('.'),
        ['', 'K', 'M', 'G', 'T', 'P'][magnitude]
    )


@register.inclusion_tag('evileg_core/drawer_item.html')
def drawer_item(title, url='#', icon=None, **kwargs):
    item_id = kwargs.pop('item_id', None)
    counter = kwargs.pop('counter', None)

    return {
        'title': title,
        'url': url,
        'icon': icon,
        'counter': human_format(counter) if counter is not None else counter,
        'item_id': 'id={}'.format(item_id) if item_id is not None else '',
        'badge': kwargs.pop('badge', 'light'),
        'visible': True if counter is not None and (kwargs.pop('always_visible', False) or counter > 0) else False,
    }
