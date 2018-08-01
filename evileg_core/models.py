# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EAbstractPost(models.Model):

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    content = models.TextField(_('Content'), blank=True)
    pub_date = models.DateTimeField(_('Publication date'), blank=True, null=True)
    lastmod = models.DateTimeField(_('Last modification date'), blank=True, null=True)

    def __str__(self):
        return self.content[:150]

    class Meta:
        abstract = True


class EModerationMixin(models.Model):

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
    class Meta:
        abstract = True


class EAbstractArticle(EAbstractPost):

    title = models.CharField(_('Title'), max_length=200, blank=True)
    views = models.IntegerField(_('Views'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class EAbstractModeratedArticle(EModerationMixin, EAbstractArticle):
    class Meta:
        abstract = True
