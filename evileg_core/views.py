# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views import View

from .mixins import EAjaxableMixin
from .utils import EMarkdownWorker


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
