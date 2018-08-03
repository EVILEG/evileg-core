# -*- coding: utf-8 -*-


from django.db import models
from django.db.models import Q


class EPostManager(models.Manager):
    """
    EPostManager is a manager for search in ESNF-C models. It is setted to EAbstractPost.
    It searches content by lookup fields, related lookup fields, author, and pub_date range
    """
    use_for_related_fields = True

    def search(self, query=None, in_related=False, user=None, date_from=None, date_to=None):
        """
        Method for search content

        :param query: search request
        :param in_related: True if you want search content by by fields in related content
        :param user: search by user
        :param date_from: "From date" for pub_date range searching
        :param date_to: "To date" for pub_date range searching
        :return: QuerySet of model objects
        """
        qs = self.get_queryset()
        if query is not None:
            or_lookup = Q()
            if self.model.lookup_fields:
                for field in self.model.lookup_fields:
                    or_lookup |= Q(**{"{}__icontains".format(field): query})

            if in_related and self.model.related_lookup_fields:
                for related_field in self.model.related_lookup_fields:
                    or_lookup |= Q(**{"{}__icontains".format(related_field): query})

            qs = qs.filter(or_lookup)

        if user is not None:
            qs = qs.filter(author=user)

        if date_from is not None and date_to is not None:
            qs = qs.filter(pub_date__range=[date_from, date_to])

        qs = qs.distinct()
        return qs
