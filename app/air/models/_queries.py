from django.db import models

from app.air.models.choices import FlightClass
from app.base.models.base import AbstractModel


class Query(AbstractModel):
    passengers = models.IntegerField()
    flight_class = models.TextField(choices=FlightClass.choices)


class QueryTrip(AbstractModel):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='trips')
    origin = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='query_trips_by_origin'
    )
    destination = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='query_trips_by_destination'
    )
    date = models.DateField()
