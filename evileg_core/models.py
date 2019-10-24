# -*- coding: utf-8 -*-

"""
Module which contains abstract models for fast development of web-site content.
It includes classes for creating content and moderation of this content
"""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from .fields import EMarkdownField
from .managers import EPostManager, EActivityManager
from .mixins import EInterfaceMixin


class EAbstractPost(models.Model):
    """
    This is base abstract class of content in the your social network. You can use this class for generating post,
    comments, messages and so on

    :param user: user of content, ForeignKey to settings.AUTH_USER_MODEL
    :param content: content, html message, django.db.models.TextField
    :param content_markdown: markdown content, which is editing by user
    :param pub_date: publication date of content, django.db.models.DateTimeField
    :param lastmod: last modification date, django.db.models.DateTimeField
    :param lookup_fields: fields for search via EPostManager
    :param related_lookup_fields: fields for search in related models via EPostManager
    """

    edit_url_name = None

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_('Content - HTML'), blank=True)
    content_markdown = EMarkdownField(verbose_name=_('Content - Markdown'), html_field='content', default='')
    pub_date = models.DateTimeField(verbose_name=_('Publication date'), blank=True, null=True, auto_now_add=True)
    lastmod = models.DateTimeField(verbose_name=_('Last modification date'), blank=True, null=True, auto_now=True)

    lookup_fields = ('content',)
    related_lookup_fields = ()

    objects = EPostManager()

    def __str__(self):
        return self.content[:150]

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, value):
        raise NotImplementedError("Implement parent setter")

    def get_title(self):
        p = self.parent
        if p:
            return p.get_title()
        raise NotImplementedError("Return title or None")

    def editable(self):
        return (timezone.now() - self.pub_date) < timezone.timedelta(days=1)

    def was_edited(self):
        return self.lastmod and (self.lastmod - self.pub_date).total_seconds() > 1

    def get_edit_url(self):
        if self.edit_url_name:
            return reverse(self.edit_url_name, kwargs={'pk': self.pk})
        raise NotImplementedError("Need implement get_edit_url or set name of url path")

    def get_self(self):
        """
        This method return object, which has view representation for rendering in template.
        For example Activity object has Foreign key to Post object, and will return Post object instead of self.

        :return: object
        """
        return self

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

    def is_approved(self):
        return self.moderation is not self.SPAM

    class Meta:
        abstract = True


class EAbstractPostWithInterface(EAbstractPost, EInterfaceMixin):
    """
    This class is the EAbstractPost with template interface
    """

    def get_preview(self):
        return self.content

    def get_meta_description(self):
        return strip_tags(self.content)[0:200]

    class Meta:
        abstract = True


class EAbstractModeratedPost(EModerationMixin, EAbstractPost):
    """
    This class is the EAbstractPost with moderation opportunity
    """
    class Meta:
        abstract = True


class EAbstractModeratedPostWithInterface(EModerationMixin, EAbstractPostWithInterface):
    """
    This class is the EAbstractPost with template interface and moderation opportunity
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
    slug = models.SlugField(_('URL'), max_length=50, blank=True)

    lookup_fields = EAbstractPost.lookup_fields + ('title',)

    def __str__(self):
        return self.get_title()

    def get_title(self):
        return self.title

    def editable(self):
        return True

    def get_subscribers_url(self):
        raise NotImplementedError('Please implement method for return url of subscribers page')

    class Meta:
        abstract = True


class EAbstractArticleWithInterface(EAbstractArticle, EInterfaceMixin):
    """
    This class is the EAbstractArticle with template interface
    """

    def get_preview(self):
        return self.content

    def get_meta_description(self):
        return "{}. {}".format(self.title, strip_tags(self.content)[0:200])

    class Meta:
        abstract = True


class EAbstractModeratedArticle(EModerationMixin, EAbstractArticle):
    """
    This class is the EAbstractArticle with moderation opportunity
    """
    class Meta:
        abstract = True


class EAbstractModeratedArticleWithInterface(EModerationMixin, EAbstractArticleWithInterface):
    """
    This class is the EAbstractArticle wtemplate interface and moderation opportunity
    """
    class Meta:
        abstract = True


class EAbstractSection(EAbstractArticle):
    class Meta:
        abstract = True


class EAbstractSectionWithInterface(EAbstractSection, EInterfaceMixin):

    def get_preview(self):
        return self.content

    def get_meta_description(self):
        return "{}. {}".format(self.title, strip_tags(self.content)[0:200])

    class Meta:
        abstract = True


class EAbstractModeratedSection(EModerationMixin, EAbstractSection):
    class Meta:
        abstract = True


class EAbstractModeratedSectionWithInterface(EModerationMixin, EAbstractSectionWithInterface):
    class Meta:
        abstract = True


class EAbstractActivity(models.Model):
    """
    Class for creating different activities like subscriptions, bookmarks, likes dislikes and so on

    :param user: User which creates made this action
    :param content_type: Django has ContentType model in which stores all types of Models of your web-site.
    :param object_id: ID of object in some table on your web-site
    :param content_object: parameter via which you can access to object
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)ss', related_query_name='%(class)ss',
                             verbose_name=_("User"), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = EActivityManager()

    def __str__(self):
        return self.content_object.__str__()[:150]

    def get_self(self):
        """
        This method return object, which has view representation for rendering in template.
        Activity object has Foreign key to Post object, and will return Post object instead of self.

        :return: object
        """
        return self.content_object

    def invalidate_cache(self):
        pass

    class Meta:
        abstract = True
