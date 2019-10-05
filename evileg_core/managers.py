# -*- coding: utf-8 -*-


from django.db import models
from django.db.models import Q


class EPostManager(models.Manager):
    """
    EPostManager is a manager for search in ESNF-C models. It is set to EAbstractPost.
    It searches content by lookup fields, related lookup fields, user, and pub_date range
    """
    use_for_related_fields = True

    def search(self, query=None, in_related=False, user=None, approved=True, date_from=None, date_to=None,
               select_related=None, prefetch_related=None,  only=None, order_by=None, distinct=False, annotation=None,
               **kwargs):
        """
        Method for search content

        :param query: search request
        :param in_related: True if you want search content by by fields in related content
        :param user: search by user
        :param approved: select only approved content
        :param date_from: "From date" for pub_date range searching
        :param date_to: "To date" for pub_date range searching
        :param select_related: list of select related query sets
        :param prefetch_related: list of prefetch related query sets
        :param order_by: list of fields for ordering
        :return: QuerySet of model objects
        """
        qs = self.approved() if approved else self.get_queryset()
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
            qs = qs.filter(user=user)

        if date_from is not None and date_to is not None:
            qs = qs.filter(pub_date__range=[date_from, date_to])

        if annotation:
            qs = qs.annotate(**annotation)

        if select_related:
            qs = qs.select_related(*select_related)

        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)

        if only:
            qs = qs.only(*only)

        if order_by:
            qs = qs.order_by(*order_by)

        if distinct:
            qs = qs.distinct()

        return qs

    def approved(self):
        """
        Method for return approved content, like is published content or moderated content
        Override it by your needs

        :return: QuerySet of model objects
        """
        return self.get_queryset()


class EActivityManager(models.Manager):
    """
    EActivityManager is a manager for search in ESNF-C activity models. It is set to EAbstractActivity.
    It searches content by lookup fields, related lookup fields, and pub_date range in targeted model
    """
    use_for_related_fields = True

    def search(self, model=None, query=None, in_related=False, date_from=None, date_to=None, approved_dict=None,
               prefetch_related=None, only=None, **kwargs):
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
            qs = qs.filter({"{}s__pub_date__range".format(model_name): [date_from, date_to]})

        if approved_dict:
            qs = qs.filter(**{"{}s__{}".format(model_name, field_name): condition for field_name, condition in approved_dict.items()})

        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)

        if only:
            qs = qs.only(*only)

        return qs

    def by_users(self, q, select_related=None, only=None):
        qs = self.get_queryset()
        if q:
            qs = qs.filter(Q(user__username__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q))

        if select_related:
            qs = qs.select_related(*select_related)

        if only:
            qs = qs.only(*only)

        return qs.order_by('user__username')
