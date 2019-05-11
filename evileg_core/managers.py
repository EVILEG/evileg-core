# -*- coding: utf-8 -*-


from django.db import models
from django.db.models import Q


class EPostManager(models.Manager):
    """
    EPostManager is a manager for search in ESNF-C models. It is set to EAbstractPost.
    It searches content by lookup fields, related lookup fields, author, and pub_date range
    """
    use_for_related_fields = True

    def search(self, query=None, in_related=False, user=None, date_from=None, date_to=None, select_related=None,
               prefetcth_related=None, **kwargs):
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

        if select_related:
            qs = qs.select_related(*select_related)

        if prefetcth_related:
            qs = qs.prefetch_related(*prefetcth_related)
        return qs


class EActivityManager(models.Manager):
    """
    EActivityManager is a manager for search in ESNF-C activity models. It is set to EAbstractActivity.
    It searches content by lookup fields, related lookup fields, and pub_date range in targeted model
    """
    use_for_related_fields = True

    def search(self, model=None, query=None, in_related=False, date_from=None, date_to=None, **kwargs):
        model_name = model.__name__.lower()
        qs = self.get_queryset().filter(content_type__model=model_name).order_by("-{}s__pub_date".format(model_name))
        if query is not None:
            or_lookup = Q()
            if model.lookup_fields:
                for field in model.lookup_fields:
                    or_lookup |= Q(**{"{}s__{}__icontains".format(model_name, field): query})

            if in_related and model.related_lookup_fields:
                for related_field in model.related_lookup_fields:
                    or_lookup |= Q(**{"{}s__{}__icontains".format(model_name, related_field): query})

            qs = qs.filter(or_lookup)

        if date_from is not None and date_to is not None:
            qs = qs.filter({"{}s__pub_date__range": [date_from, date_to]})

        return qs

    def by_users(self, q):
        if q:
            return self.get_queryset().filter(Q(user__username__icontains=q) | Q(user__first_name__icontains=q) | Q(
                user__last_name__icontains=q)).order_by('user__username')
        return self.get_queryset().order_by('user__username')
