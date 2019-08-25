# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .filters import EDateRangeFilter


class EModerationMixinAdmin(admin.ModelAdmin):
    """
    Mixin for representation table in Django administration panel with content which includes moderation opportunity
    """
    list_display = ('moderation',)
    list_filter = ('moderation',)
    actions = ['make_spam', 'make_not_moderated', 'make_post_moderated', 'make_moderated']

    def moderate(self, request, rows_updated, choice_description):
        """
        Common method for representation of marking result

        :param request: HTTP request
        :param rows_updated: count of updated ibjects
        :param choice_description: SPAM, NOT MODERATED, POST MODERATED or MODERATED
        """
        if rows_updated == 1:
            message_bit = "1 entry is marked as %s" % choice_description
        else:
            message_bit = "%s entries are marked as %s." % (rows_updated, choice_description)
        self.message_user(request, "%s" % message_bit)

    def make_spam(self, request, queryset):
        """
        Action for marking content like SPAM

        :param request: HTTP request
        :param queryset: queryset of model objects
        """
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.SPAM),
            choice_description=_("SPAM")
        )

    make_spam.short_description = _("Set marked as SPAM")

    def make_not_moderated(self, request, queryset):
        """
        Action for marking content like NOT MODERATED

        :param request: HTTP request
        :param queryset: queryset of model objects
        """
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.NOT_MODERATED),
            choice_description=_("NOT MODERATED")
        )

    make_not_moderated.short_description = _("Set marked as NOT MODERATED")

    def make_post_moderated(self, request, queryset):
        """
        Action for marking content like POST MODERATED

        :param request: HTTP request
        :param queryset: queryset of model objects
        """
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.POST_MODERATED),
            choice_description=_("POST MODERATED")
        )

    make_post_moderated.short_description = _("Set marked as POST MODERATED")

    def make_moderated(self, request, queryset):
        """
        Action for marking content like MODERATED

        :param request: HTTP request
        :param queryset: queryset of model objects
        """
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.MODERATED),
            choice_description=_("MODERATED")
        )

    make_moderated.short_description = _("Set marked as MODERATED")


class EPostAdmin(admin.ModelAdmin):
    """
    Base class for representation table in Django administration panel.
    This class is designed for classes which inherits from evileg_core.models.EAbstractPost
    """
    list_display = ('__str__', 'user', 'pub_date', 'lastmod')
    list_filter = (('pub_date', EDateRangeFilter),)
    autocomplete_fields = ['user']
    search_fields = ('content', 'user__username')
    readonly_fields = ('pub_date', 'lastmod')
    fields = ['user', 'content_markdown', 'pub_date', 'lastmod']


class EPostModeratedAdmin(EModerationMixinAdmin, EPostAdmin):
    """
    This class is the EPostAdmin with moderation opportunity
    """
    list_display = EPostAdmin.list_display + EModerationMixinAdmin.list_display
    list_filter = EPostAdmin.list_filter + EModerationMixinAdmin.list_filter


class EArticleAdmin(EPostAdmin):
    """
    Base class for representation table in Django administration panel.
    This class is designed for classes which inherits from evileg_core.models.EAbstractArticle
    """
    list_display = EPostAdmin.list_display + ('views',)
    search_fields = EPostAdmin.search_fields + ('title',)
    fields = ['user', 'title', 'content_markdown', 'slug', 'pub_date', 'lastmod']


class EArticleModeratedAdmin(EModerationMixinAdmin, EArticleAdmin):
    """
    This class is the EArticleAdmin with moderation opportunity
    """
    list_display = EArticleAdmin.list_display + EModerationMixinAdmin.list_display
    list_filter = EArticleAdmin.list_filter + EModerationMixinAdmin.list_filter


class ESectionAdmin(EArticleAdmin):
    """
    Base class for representation table in Django administration panel.
    This class is designed for classes which inherits from evileg_core.models.EAbstractSection
    """
    list_display = EArticleAdmin.list_display
    list_filter = EArticleAdmin.list_filter


class ESectionModeratedAdmin(EModerationMixinAdmin, ESectionAdmin):
    """
    This class is the ESectionAdmin with moderation opportunity
    """
    list_display = ESectionAdmin.list_display + EModerationMixinAdmin.list_display
    list_filter = ESectionAdmin.list_filter + EModerationMixinAdmin.list_filter
