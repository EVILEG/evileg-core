# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EAbstractPost(models.Model):

    class Meta:
        abstract = True

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    content = models.TextField(_('Content'), blank=True)
    pub_date = models.DateTimeField(_('Publication date'), blank=True, null=True)
    lastmod = models.DateTimeField(_('Last modification date'), blank=True, null=True)
