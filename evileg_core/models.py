# -*- coding: utf-8 -*-

"""
Module which contains abstract models for fast development of web-site content.
It includes classes for creating content and moderation of this content
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EAbstractPost(models.Model):
    """
    This is base abstract class of content in the your social network. You can use this class for generating post,
    comments, messages and so on

    :param author: author of content, ForeignKey to django.contrib.auth.models.User
    :param content: content, html message, django.db.models.TextField
    :param pub_date: publication date of content, django.db.models.DateTimeField
    :param lastmod: last modification date, django.db.models.DateTimeField
    """

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    content = models.TextField(_('Content'), blank=True)
    pub_date = models.DateTimeField(_('Publication date'), blank=True, null=True)
    lastmod = models.DateTimeField(_('Last modification date'), blank=True, null=True)

    def __str__(self):
        return self.content[:150]

    class Meta:
        abstract = True


class EModerationMixin(models.Model):
    """
    Moderation abstract mixin for content which should be moderated of web-site administration

    :param SPAM: mark content like spam (constant variable)
    :param NOT_MODERATED: mark content like not yet moderated (constant variable)
    :param POST_MODERATED: mark content like may be published with post moderation (constant variable)
    :param MODERATED: mark content like moderated (constant variable)
    :param MODERATION_CHOICES: choices of moderation status
    :param moderation: variable which stores moderation status
    """

    SPAM = 'S'
    NOT_MODERATED = 'N'
    POST_MODERATED = 'P'
    MODERATED = 'M'
    MODERATION_CHOICES = (
        (SPAM, _('SPAM')),
        (NOT_MODERATED, _('Not Moderated')),
        (POST_MODERATED, _('Post Moderated')),
        (MODERATED, _('Moderated'))
    )

    moderation = models.CharField(
        _('Moderation'),
        max_length=1,
        choices=MODERATION_CHOICES,
        default=NOT_MODERATED
    )

    class Meta:
        abstract = True


class EAbstractModeratedPost(EAbstractPost, EModerationMixin):
    """
    This class is the EAbstractPost with moderation opportunity
    """
    class Meta:
        abstract = True


class EAbstractArticle(EAbstractPost):
    """
    Class for articles or similar content

    :param title: Title of your article
    :param views: you can want to count all views of article
    """

    title = models.CharField(_('Title'), max_length=200, blank=True)
    views = models.IntegerField(_('Views'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class EAbstractModeratedArticle(EModerationMixin, EAbstractArticle):
    """
    This class is the EAbstractArticle with moderation opportunity
    """
    class Meta:
        abstract = True
