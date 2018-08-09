# -*- coding: utf-8 -*-

from django.conf import settings


class EInterfaceMixin:
    TEMPLATE_FULL = getattr(settings, "TEMPLATE_FULL", 'evileg_core/objects/full.html')
    TEMPLATE_PREVIEW = getattr(settings, "TEMPLATE_PREVIEW", 'evileg_core/objects/preview.html')
    TEMPLATE_INFO = getattr(settings, "TEMPLATE_INFO", 'evileg_core/objects/info.html')
    TEMPLATE_MAIL = getattr(settings, "TEMPLATE_MAIL", 'evileg_core/objects/mail.html')

    def get_title(self):
        raise NotImplementedError("Please return title or related information about title")

    def get_preview(self):
        raise NotImplementedError("Please return short information about object")

    def get_parent(self):
        raise NotImplementedError("Please return parent object or None")


class EAjaxableMixin:

    def get(self, request, *args, **kwargs):
        handler = getattr(self, 'get_ajax' if request.is_ajax() else 'get_common', self.http_method_not_allowed)
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        handler = getattr(self, 'post_ajax' if request.is_ajax() else 'post_common', self.http_method_not_allowed)
        return handler(request, *args, **kwargs)
