from django.db.models import Count, Prefetch

from app.air.components.entities.query import QueryEntity, QueryTripEntity
from app.air.models import Query, QueryTrip


class QueryManager:
    def create(self, query_entity: QueryEntity) -> Query:
        if query := self.get(query_entity):
            return query
        query = Query.objects.create(
            passengers=query_entity.passengers, flight_class=query_entity.flight_class
        )
        for trip in query_entity.trips:
            QueryTrip.objects.create(query=query, **dict(trip))
        return query
    
    def get(self, query_entity: QueryEntity) -> Query | None:
        applicants = Query.objects.annotate(trips_count=Count('trips')).filter(
            passengers=query_entity.passengers, flight_class=query_entity.flight_class,
            trips_count=len(query_entity.trips)
        ).prefetch_related(Prefetch('trips', QueryTrip.objects.order_by('date')))
        for applicant in applicants:
            is_next_applicant = False
            for trip, applicant_trip in zip(query_entity.trips, applicant.trips.all()):
                if trip != QueryTripEntity.from_model(applicant_trip):
                    is_next_applicant = True
                    break
            if is_next_applicant:
                continue
            return applicant
        return None
