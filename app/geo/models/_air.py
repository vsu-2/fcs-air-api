from django.db import models

from app.geo.models._locations import City
from app.geo.models.base import _AbstractGeoModel


class Airport(_AbstractGeoModel):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='airports',
        # related_query_name='airport'
    )


class Airline(_AbstractGeoModel):
    pass
