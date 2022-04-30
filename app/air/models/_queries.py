from django.db import models

from app.air.models.choices import FlightClass
from app.base.models.base import AbstractModel


class Query(AbstractModel):
    flight_class = models.PositiveSmallIntegerField(choices=FlightClass.choices)


class QueryTrip(AbstractModel):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    origin = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='querytrip_by_origin'
    )
    destination = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='querytrip_by_destination'
    )
    date = models.DateField()
