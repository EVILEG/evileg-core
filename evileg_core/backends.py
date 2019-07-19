# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.db.models import Q

from evileg_core.shortcuts import get_object_or_none


class EEmailOrUsernameModelBackend:
    """
    Authentication backend for using email or username for authentication on the site.
    """
    def authenticate(self, request, username=None, password=None):
        """

        :param request: HTTP Request
        :param username: username of email
        :param password: password
        :return: User Object or None
        """
        user = get_object_or_none(get_user_model(), Q(username__exact=username) | Q(email__exact=username))
        return user if user and user.check_password(password) else None

    def get_user(self, user_id):
        """
        Function for get authenticated user

        :param user_id: id of user in database
        :return: User Object or None
        """
        return get_object_or_none(get_user_model(), pk=user_id)
