from django.db import models

from app.geo.models.base import _AbstractGeoModel


class Country(_AbstractGeoModel):
    pass


class City(_AbstractGeoModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
