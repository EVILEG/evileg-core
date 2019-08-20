# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from evileg_core.shortcuts import get_object_or_none


class EEmailOrUsernameModelBackend:
    """
    Authentication backend for using email or username for authentication on the site.
    """

    def validate_email(self, email):
        """
        Check if email is really email

        :param email: email
        :return: email or None
        """
        try:
            validate_email(email)
            return email
        except ValidationError:
            return None

    def authenticate(self, request, username=None, password=None):
        """

        :param request: HTTP Request
        :param username: username or email
        :param password: password
        :return: User Object or None
        """
        email = self.validate_email(username)
        if email:
            user = get_object_or_none(get_user_model(), Q(email__exact=username))
            if user and user.check_password(password):
                return user

        user = get_object_or_none(get_user_model(), Q(username__exact=username))
        return user if user and user.check_password(password) else None

    def get_user(self, user_id):
        """
        Function for get authenticated user

        :param user_id: id of user in database
        :return: User Object or None
        """
        return get_object_or_none(get_user_model(), pk=user_id)
