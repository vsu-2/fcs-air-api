from django import forms
from django.db.models import *
from django_filters import filters

from app.base.filters.base import ArrayFilter
from app.base.filters.filtersets.base import BaseFilterSet
from app.geo.models import *
from app.tickets.models import *


class TicketsSessionsDetailTicketsFilter(BaseFilterSet):
    transfers__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_transfers__in',
        label='type: comma separated ints - numbers of transfers'
    )
    start_time__lte = filters.TimeFilter(method='filter_start_time__lte')
    start_time__gte = filters.TimeFilter(method='filter_start_time__gte')
    end_time__lte = filters.TimeFilter(method='filter_end_time__lte')
    end_time__gte = filters.TimeFilter(method='filter_end_time__gte')
    airlines__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_airlines__in',
        label='type: comma separated ints - ids of airlines'
    )
    airports__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_airports__in',
        label='type: comma separated ints - ids of airports'
    )
    offers__in = ArrayFilter(
        base_field=forms.IntegerField(), method='filter_offers__in',
        label='type: comma separated ints - gate_ids if offers'
    )
    
    class Meta:
        model = Ticket
        fields = {'travel_time': ['lte', 'gte']}
    
    @staticmethod
    def filter_transfers__in(queryset, _, value):
        return queryset.annotate(
            # ищем самое большое количество сегментов среди всех рейсов билета
            max_segment_count=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id')).annotate(
                    Count('segment')
                ).order_by('-segment__count').values('segment__count')[:1]
            )
        ).filter(
            # сегментов всегда на 1 больше, чем пересадок
            max_segment_count__in=map(lambda v: v + 1, value)
        )
    
    @staticmethod
    def filter_start_time__lte(queryset, _, value):
        return queryset.annotate(
            # ищем время вылета первого рейса
            start_time=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id'), number=0).values(
                    'start_time'
                )[:1]
            )
        ).filter(start_time__time__lte=value)
    
    @staticmethod
    def filter_start_time__gte(queryset, _, value):
        # аналогично filter_start_time__lte, но с gte
        return queryset.annotate(
            start_time=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id'), number=0).values(
                    'start_time'
                )[:1]
            )
        ).filter(start_time__time__gte=value)
    
    @staticmethod
    def filter_end_time__lte(queryset, _, value):
        return queryset.annotate(
            # ищем время вылета последнего рейса
            end_time=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id')).order_by('-number').values(
                    'end_time'
                )[:1]
            )
        ).filter(end_time__time__lte=value)
    
    @staticmethod
    def filter_end_time__gte(queryset, _, value):
        # аналогично filter_end_time__lte, но с gte
        return queryset.annotate(
            end_time=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id')).order_by('-number').values(
                    'end_time'
                )[:1]
            )
        ).filter(end_time__time__gte=value)
    
    @staticmethod
    def filter_airlines__in(queryset, _, value):
        return queryset.annotate(
            # находим рейс с хотя бы одним сегментом, авиакомпании которого нет среди
            # искомых, если есть (иначе null)
            trip_with_other_airline=Subquery(
                Trip.objects.filter(ticket_id=OuterRef('id')).annotate(
                    # находим сегмент с авиакомпанией, которой нет среди искомых,
                    # если есть (иначе null)
                    segment_with_other_airline=Subquery(
                        Segment.objects.filter(
                            trip_id=OuterRef('id')
                        ).exclude(about__airline_id__in=value).values('id')[:1]
                    )
                ).filter(segment_with_other_airline__isnull=False).values('id')[:1]
            )
        ).filter(trip_with_other_airline__isnull=True)
    
    @staticmethod
    def filter_airports__in(queryset, _, value):
        return queryset.annotate(
            # ищем рейс, в котором есть сегмент с другим аэропортом
            trip_with_other_airport=Subquery(
                Trip.objects.filter(ticket=OuterRef('id')).annotate(
                    # ищем сегмент, в котором одна из конечных точек содержит аэропорт,
                    # которого нет среди искомых
                    segment_with_other_airport=Subquery(
                        Segment.objects.filter(trip=OuterRef('id')).annotate(
                            other_airport=Subquery(
                                Airport.objects.filter(
                                    # рассматриваем аэропорты, являющиеся конечными
                                    # точками сегмента
                                    Q(segments_by_arrival=OuterRef('id')) |
                                    Q(segments_by_departure=OuterRef('id'))
                                ).exclude(
                                    id__in=value
                                ).distinct().values('id')[:1]
                            )
                        ).filter(other_airport__isnull=False).values('id')[:1]
                    )
                ).filter(segment_with_other_airport__isnull=False).values('id')[:1]
            )
        ).filter(trip_with_other_airport__isnull=True)
    
    @staticmethod
    def filter_offers__in(queryset, _, value):
        return queryset.filter(offer__gate_id__in=value)
