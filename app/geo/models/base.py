from django.db import models

from app.base.models.base import AbstractModel


class _AbstractGeoModel(AbstractModel):
    code = models.TextField(unique=True)
    title = models.TextField()
    
    class Meta:
        abstract = True
