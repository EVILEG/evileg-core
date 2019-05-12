# -*- coding: utf-8 -*-

import re
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.utils.translation import (
    LANGUAGE_SESSION_KEY,
    check_for_language
)
from django.views import View

from .mixins import EAjaxableMixin
from .utils import EMarkdownWorker, get_next_url


class EMarkdownView(View):
    """
    Markdown view for preview html content
    """
    def post(self, request):
        return JsonResponse({'preview': EMarkdownWorker(request.POST.get('content')).get_text()})


class EAjaxableView(EAjaxableMixin, View):
    """
    Ajaxable view
    """
    pass


def lang(request, lang_code):
    """
    Switch to selected language by link

    **Example**::

        <a href="{% url 'lang' 'en' %}">English</a>

    :param request: HTTP Request
    :param lang_code: 'en' or 'ru'
    :return: HTTP Response
    """
    next = request.POST.get('next', request.GET.get('next'))
    if (next or not request.is_ajax()) and not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = get_next_url(request)
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)

    if lang_code and check_for_language(lang_code):
        if next:
            for code_tuple in settings.LANGUAGES:
                settings_lang_code = "/" + code_tuple[0]
                parsed = urlsplit(next)
                if parsed.path.startswith(settings_lang_code):
                    path = re.sub('^' + settings_lang_code, '', parsed.path)
                    next = urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
            response = HttpResponseRedirect(next)
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )
    return response
