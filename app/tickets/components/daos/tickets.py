from django.db.models import Prefetch, QuerySet

from app.geo.models import Airport
from app.tickets.models import *


class TicketsDao:
    def prefetch(self, queryset: QuerySet = Ticket.objects.all()) -> QuerySet:
        return queryset.prefetch_related(
            'best_offer',
            Prefetch(
                'trips', Trip.objects.prefetch_related(
                    'origin', 'destination', Prefetch(
                        'segments', Segment.objects.prefetch_related(
                            'marketing_airline',
                            Prefetch(
                                'departure', Airport.objects.prefetch_related('city')
                            ),
                            Prefetch('arrival', Airport.objects.prefetch_related('city'))
                        ).order_by('departure_time')
                    )
                ).order_by('number')
            )
        ).exclude(best_offer=None).nocache()
