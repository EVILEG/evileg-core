# -*- coding: utf-8 -*-

from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin

from .forms import EActionForm

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

    def get_preview(self, *args, **kwargs):
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


class EPaginateMixin:
    """
    Mixin for adding page pagination functionality into Class Based View.
    Mixin support get and post requests
    """
    def get_paginated_page(self, objects, number=10):
        """
        Method get queryset for creating paginated page by page number form request

        :param objects: QuerySet or objects list
        :param number: number of objects on the page
        :return: page with objects
        """
        return Paginator(objects, number).get_page(
            self.request.GET.get('page') if self.request.method == 'GET' else self.request.POST.get('page'))

    def get_pagination_url(self):
        """
        Method for creating pagination url for bootstrap_pagination from django-bootstrap4

        :return: pagination url
        """
        return self.request.get_full_path().replace(self.request.path, '')


class EUpCounterMixin:
    counter_field_name = 'views'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if hasattr(self.object, self.counter_field_name):
            setattr(self.object, self.counter_field_name, getattr(self.object, self.counter_field_name, 0) + 1)
            self.object.save(update_fields=[self.counter_field_name])
        return response


class EBreadCrumbListMixin:

    def get_breadcrumb_list(self, **kwargs):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'breadcrumb_list': self.get_breadcrumb_list(**kwargs)})
        return context


class EInUserProfileMixin:
    user_profile = None

    def dispatch(self, request, *args, **kwargs):
        self.user_profile = get_object_or_404(get_user_model(), username=kwargs['user'], is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
            'user_profile': self.user_profile
        })
        return context


class EActionFormMixin:
    actions = None
    action_form = EActionForm

    def get_action(self, action):
        """
        Return a given action from a parameter, which can either be a callable,
        or the name of a method on the Mixin.  Return is a tuple of
        (callable, name, description).
        """
        # If the action is a callable, just use it.
        if callable(action):
            func = action
            action = action.__name__

        # Next, look for a method. Grab it off self.__class__ to get an unbound
        # method instead of a bound one; this ensures that the calling
        # conventions are the same for functions and methods.
        elif hasattr(self.__class__, action):
            func = getattr(self.__class__, action)

        if hasattr(func, 'short_description'):
            description = func.short_description
        else:
            description = capfirst(action.replace('_', ' '))
        return func, action, description

    def _get_base_actions(self):
        """Return the list of actions, prior to any request-based filtering."""
        actions = []

        # Add actions
        actions.extend(self.get_action(action) for action in self.actions or [])
        # get_action might have returned None, so filter any of those out.
        return filter(None, actions)

    def _filter_actions_by_permissions(self, request, actions):
        """Filter out any actions that the user doesn't have access to."""
        filtered_actions = []
        for action in actions:
            callable = action[0]
            if not hasattr(callable, 'allowed_permissions'):
                filtered_actions.append(action)
                continue
            permission_checks = (
                getattr(self, 'has_%s_permission' % permission)
                for permission in callable.allowed_permissions
            )
            if any(has_permission(request) for has_permission in permission_checks):
                filtered_actions.append(action)
        return filtered_actions

    def get_actions(self, request):
        """
        Return a dictionary mapping the names of all actions for this
        Mixin to a tuple of (callable, name, description) for each action.
        """
        # If self.actions is set to None that means actions are disabled on
        # this page.
        if self.actions is None:
            return OrderedDict()
        actions = self._filter_actions_by_permissions(request, self._get_base_actions())
        # Convert the actions into an OrderedDict keyed by name.
        return OrderedDict(
            (name, (func, name, desc))
            for func, name, desc in actions
        )

    def get_action_choices(self, request, default_choices=BLANK_CHOICE_DASH):
        """
        Return a list of choices for use in a form object.  Each choice is a
        tuple (name, description).
        """
        choices = [] + default_choices
        for func, name, description in self.get_actions(request).values():
            choices.append((name, description))
        return choices

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                     fail_silently=False):
        """
        Send a message to the user. The default implementation
        posts a message using the django.contrib.messages backend.

        Exposes almost the same API as messages.add_message(), but accepts the
        positional arguments in a different order to maintain backwards
        compatibility. For convenience, it accepts the `level` argument as
        a string rather than the usual level number.
        """
        if not isinstance(level, int):
            # attempt to get the level if passed a string
            try:
                level = getattr(messages.constants, level.upper())
            except AttributeError:
                levels = messages.constants.DEFAULT_TAGS.values()
                levels_repr = ', '.join('`%s`' % l for l in levels)
                raise ValueError(
                    'Bad message level string: `%s`. Possible values are: %s'
                    % (level, levels_repr)
                )

        messages.add_message(request, level, message, extra_tags=extra_tags, fail_silently=fail_silently)

    def response_action(self, request, queryset):
        """
        Handle an action. This is called if a request is POSTed to the
        changelist; it returns an HttpResponse if the action was handled, and
        None otherwise.
        """

        # There can be multiple action forms on the page (at the top
        # and bottom of the change list, for example). Get the action
        # whose button was pushed.
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop('object_id', None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            # If we didn't get an action from the chosen form that's invalid
            # POST data, so by deleting action it'll fail the validation check
            # below. So no need to do anything here
            pass

        action_form = self.action_form(data, auto_id=None)
        action_form.fields['action'].choices = self.get_action_choices(request)

        # If the form's valid we can handle the action.
        if action_form.is_valid():
            action = action_form.cleaned_data['action']
            select_across = action_form.cleaned_data['select_across']
            func = self.get_actions(request)[action][0]

            # Get the list of selected PKs. If nothing's selected, we can't
            # perform an action on it, so bail. Except we want to perform
            # the action explicitly on all objects.
            selected = request.POST.getlist('object_id')
            if not selected and not select_across:
                # Reminder that something needs to be selected or nothing will happen
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                return None

            if not select_across:
                # Perform the action only on the selected objects
                queryset = queryset.filter(pk__in=selected)

            response = func(self, request, queryset)

            # Actions may return an HttpResponse-like object, which will be
            # used as the response from the POST. If not, we'll be a good
            # little HTTP citizen and redirect back to the changelist page.
            if isinstance(response, HttpResponseBase):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            msg = _("No action selected.")
            self.message_user(request, msg, messages.WARNING)
            return None

    def post(self, request, *args, **kwargs):
        response = self.response_action(request, queryset=self.get_queryset(**kwargs))
        if response:
            return response

        if hasattr(super(), 'post'):
            return super().post(request, *args, **kwargs)
        return render(request=request, template_name=self.template_name, context=self.get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(self.request)
        else:
            action_form = None

        context = super().get_context_data(**kwargs)
        context.update({
            'action_form': action_form,
        })
        return context
