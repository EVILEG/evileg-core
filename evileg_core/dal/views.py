# -*- coding: utf-8 -*-

from dal import autocomplete


class EGenericAutocomplete(autocomplete.Select2QuerySetView):
    queryset = None
    fields = None

    def get_queryset(self):
        qs = self.queryset
        return qs.filter(**{key: self.q for key in self.fields}) if self.q and self.fields else qs
