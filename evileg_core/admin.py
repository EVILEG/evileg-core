# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .filters import EDateRangeFilter


class EPostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'pub_date', 'lastmod')
    list_filter = (('pub_date', EDateRangeFilter),)
    autocomplete_fields = ['author']
    search_fields = ('content', 'author__username')


class EModerationMixinAdmin(admin.ModelAdmin):
    list_display = ('moderation',)
    list_filter = ('moderation',)
    actions = ['make_spam', 'make_not_moderated', 'make_post_moderated', 'make_moderated']

    def moderate(self, request, rows_updated, choice_description):
        if rows_updated == 1:
            message_bit = "1 entry is marked as %s" % choice_description
        else:
            message_bit = "%s entries are marked as %s." % (rows_updated, choice_description)
        self.message_user(request, "%s" % message_bit)

    def make_spam(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.SPAM),
            choice_description=_("SPAM")
        )

    make_spam.short_description = _("Set marked as SPAM")

    def make_not_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.NOT_MODERATED),
            choice_description=_("NOT MODERATED")
        )

    make_not_moderated.short_description = _("Set marked as NOT MODERATED")

    def make_post_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.POST_MODERATED),
            choice_description=_("POST MODERATED")
        )

    make_post_moderated.short_description = _("Set marked as POST MODERATED")

    def make_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=self.model.MODERATED),
            choice_description=_("MODERATED")
        )

    make_moderated.short_description = _("Set marked as MODERATED")


class EPostModeratedAdmin(EModerationMixinAdmin, EPostAdmin):
    list_display = EPostAdmin.list_display + EModerationMixinAdmin.list_display
    list_filter = EPostAdmin.list_filter + EModerationMixinAdmin.list_filter


class EArticleAdmin(EPostAdmin):
    list_display = EPostAdmin.list_display + ('views',)
    search_fields = EPostAdmin.search_fields + ('title',)


class EArticleModeratedAdmin(EModerationMixinAdmin, EArticleAdmin):
    list_display = EArticleAdmin.list_display + EModerationMixinAdmin.list_display
    list_filter = EArticleAdmin.list_filter + EModerationMixinAdmin.list_filter
