# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin


_interface_templates_cache = {}


class EInterfaceMixin:
    """
    Interface Mixin for representation object in the templates.
    It is needed to creating a uniform interface in all content objects.

    All content objects has several types of representation.

    You can override this template in class of content, or globally in the settings.py of your django project.

    :param TEMPLATE_FULL: full template representation
    :param TEMPLATE_PREVIEW: preview template representation
    :param TEMPLATE_INFO: information template representation, commonly it has smaller info than TEMPLATE_PREVIEW
    :param TEMPLATE_MAIL: template representation for rendering this content in mail
    """
    TEMPLATE_FULL = getattr(settings, "TEMPLATE_FULL", 'evileg_core/objects/full.html')
    TEMPLATE_PREVIEW = getattr(settings, "TEMPLATE_PREVIEW", 'evileg_core/objects/preview.html')
    TEMPLATE_INFO = getattr(settings, "TEMPLATE_INFO", 'evileg_core/objects/info.html')
    TEMPLATE_MAIL = getattr(settings, "TEMPLATE_MAIL", 'evileg_core/objects/mail.html')

    edit_url_name = None

    def get_title(self):
        p = self.parent
        if p:
            return p.get_title()
        raise NotImplementedError("Return title or None")

    def get_preview(self):
        raise NotImplementedError("Please return short information about object")

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, value):
        raise NotImplementedError("Implement parent setter")

    def get_meta_description(self):
        raise NotImplementedError("Please return meta description about content or None")

    def was_edited(self):
        raise NotImplementedError("Please return information if object was edited")

    def editable(self):
        raise NotImplementedError("Please add editable condition or return True")

    def get_edit_url(self):
        if self.edit_url_name:
            return reverse(self.edit_url_name, kwargs={'pk': self.pk})
        raise NotImplementedError("Need implement get_edit_url or set name of url path")

    def get_self(self):
        raise NotImplementedError("Please return self or related object for representation")

    @classmethod
    def __render_template_full(cls, obj, request_context):
        if cls.TEMPLATE_FULL not in _interface_templates_cache:
            _interface_templates_cache[cls.TEMPLATE_FULL] = loader.get_template(cls.TEMPLATE_FULL)
        return _interface_templates_cache[cls.TEMPLATE_FULL].render({'object': obj, 'user': request_context['user']})

    def render_template_full(self, request_context):
        return self.__render_template_full(self, request_context)

    @classmethod
    def __render_template_preview(cls, obj, request_context):
        if cls.TEMPLATE_PREVIEW not in _interface_templates_cache:
            _interface_templates_cache[cls.TEMPLATE_PREVIEW] = loader.get_template(cls.TEMPLATE_PREVIEW)
        return _interface_templates_cache[cls.TEMPLATE_PREVIEW].render({'object': obj, 'user': request_context['user']})

    def render_template_preview(self, request_context):
        return self.__render_template_preview(self, request_context)

    @classmethod
    def __render_template_info(cls, obj, request_context):
        if cls.TEMPLATE_INFO not in _interface_templates_cache:
            _interface_templates_cache[cls.TEMPLATE_INFO] = loader.get_template(cls.TEMPLATE_INFO)
        return _interface_templates_cache[cls.TEMPLATE_INFO].render({'object': obj, 'user': request_context['user']})

    def render_template_info(self, request_context):
        return self.__render_template_info(self, request_context)

    @classmethod
    def __render_template_mail(cls, obj):
        if cls.TEMPLATE_MAIL not in _interface_templates_cache:
            _interface_templates_cache[cls.TEMPLATE_MAIL] = loader.get_template(cls.TEMPLATE_MAIL)
        return _interface_templates_cache[cls.TEMPLATE_MAIL].render({'object': obj})

    def render_template_mail(self):
        return self.__render_template_mail(self)


class EAjaxableMixin:
    """
    Ajaxable mixin for adding ajax methods to view.
    If method not exists, then try to invoke common method.
    For example, call get_ajax() for ajax request if this method exists, otherwise call get() method
    """

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


class EPostFormMixin(FormMixin):
    """
    Mixin for call form_valid() and from_invalid() methods for post requests
    """
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)