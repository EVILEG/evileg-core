# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.template import loader


class EInterfaceMixin:
    TEMPLATE_FULL = getattr(settings, "TEMPLATE_FULL", 'evileg_core/objects/full.html')
    TEMPLATE_PREVIEW = getattr(settings, "TEMPLATE_PREVIEW", 'evileg_core/objects/preview.html')
    TEMPLATE_INFO = getattr(settings, "TEMPLATE_INFO", 'evileg_core/objects/info.html')
    TEMPLATE_MAIL = getattr(settings, "TEMPLATE_MAIL", 'evileg_core/objects/mail.html')

    template_full = None
    template_preview = None
    template_info = None
    template_mail = None

    def get_title(self):
        raise NotImplementedError("Please return title or related information about title")

    def get_preview(self):
        raise NotImplementedError("Please return short information about object")

    def get_parent(self):
        raise NotImplementedError("Please return parent object or None")

    def get_meta_description(self):
        raise NotImplementedError("Please return meta description about content or None")

    def was_edited(self):
        raise NotImplementedError("Please return information if object was edited")

    def editable(self):
        raise NotImplementedError("Please add editable condition or return True")

    @classmethod
    def __render_template_full(cls, obj, request_context):
        if not cls.template_full:
            cls.template_full = loader.get_template(cls.TEMPLATE_FULL)
        return cls.template_full.render({'object': obj, 'user': request_context['user']})

    def render_template_full(self, request_context):
        return self.__render_template_full(self, request_context)

    @classmethod
    def __render_template_preview(cls, obj, request_context):
        if not cls.template_preview:
            cls.template_preview = loader.get_template(cls.TEMPLATE_PREVIEW)
        return cls.template_preview.render({'object': obj, 'user': request_context['user']})

    def render_template_preview(self, request_context):
        return self.__render_template_preview(self, request_context)

    @classmethod
    def __render_template_info(cls, obj, request_context):
        if not cls.template_info:
            cls.template_info = loader.get_template(cls.TEMPLATE_INFO)
        return cls.template_info.render({'object': obj, 'user': request_context['user']})

    def render_template_info(self, request_context):
        return self.__render_template_info(self, request_context)

    @classmethod
    def __render_template_mail(cls, obj):
        if not cls.template_mail:
            cls.template_mail = loader.get_template(cls.TEMPLATE_MAIL)
        return cls.template_mail.render({'object': obj})

    def render_template_mail(self):
        return self.__render_template_mail(self)

    @models.permalink
    def get_edit_url(self):
        return None


class EAjaxableMixin:

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            if request.is_ajax():
                handler = getattr(self,
                                  '{}_ajax'.format(request.method.lower()),
                                  getattr(self, request.method.lower(), self.http_method_not_allowed))
            else:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
