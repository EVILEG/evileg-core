# -*- coding: utf-8 -*-

from django.contrib import admin


class EPostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'pub_date', 'lastmod')
    autocomplete_fields = ['author']
    search_fields = ('content', 'author__username')
