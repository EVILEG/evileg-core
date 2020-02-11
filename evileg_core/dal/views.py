# -*- coding: utf-8 -*-

from dal import autocomplete
from tagging.models import Tag


class ETagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        return qs.filter(name__istartswith=self.q) if self.q else qs
