from django.db import models

from app.geo.models._places import City
from app.geo.models.base import _AbstractGeoModel


class Airport(_AbstractGeoModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Airline(_AbstractGeoModel):
    pass
