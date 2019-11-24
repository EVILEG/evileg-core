# -*- coding: utf-8 -*-

import re
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import is_safe_url
from django.utils.translation import LANGUAGE_SESSION_KEY, check_for_language
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin

from .mixins import EAjaxableMixin, EPaginateMixin
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


class EPaginatedView(ContextMixin, EPaginateMixin, EAjaxableView):
    model = None
    queryset = None
    template_name = None
    template_partials_name = 'evileg_core/partials/object_list_preview.html'
    paginated_by = 10
    by_user = False
    columns_view = False

    def get_user(self, **kwargs):
        username = kwargs.pop('user', None)
        if username:
            return get_object_or_404(get_user_model(), username=username, is_active=True)
        else:
            return self.request.user

    def get_queryset(self, **kwargs):
        qs = None
        if self.queryset:
            qs = self.queryset.all()
        elif self.model and qs is None:
            qs = self.model.objects.all()
        else:
            return qs

        if self.by_user:
            qs = qs.filter(user=self.get_user(**kwargs))
        return qs

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context=self.get_context_data(**kwargs))

    def get_ajax(self, request, *args, **kwargs):
        return JsonResponse({
            'object_list': render_to_string(
                request=request,
                template_name=self.template_partials_name,
                context=self.get_context_data(**kwargs)
            ),
        })

    def _get_context_data(self, **kwargs):
        qs = self.get_queryset(**kwargs)
        return {
            'object_list': self.get_paginated_page(qs, self.paginated_by) if qs else None,
            'last_question': self.get_pagination_url(),
            'columns_view': self.columns_view
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_context_data(**kwargs))
        return context


class EFilterView(EPaginatedView):
    model_filter = None

    def _get_context_data(self, **kwargs):
        data = self.request.GET if self.request.method == 'GET' else self.request.POST
        f = self.model_filter(data, queryset=self.get_queryset(**kwargs))
        return {
            'object_list': self.get_paginated_page(f.qs, self.paginated_by),
            'last_question': self.get_pagination_url(),
            'search_filter': f,
            'columns_view': self.columns_view
        }


class EFilterDetailView(EFilterView, DetailView):
    object_queryset = None
    object_pk_field_name = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get_ajax(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return super().get_object(queryset=self.object_queryset)

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(**{self.object_pk_field_name: self.object.pk}) if qs else qs
