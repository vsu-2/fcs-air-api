from django.db import models

from app.air.models import Query
from app.base.models.base import AbstractModel
from app.users.models import User


class Favorite(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='favorites')
    
    class Meta(AbstractModel.Meta):
        unique_together = ('user', 'query')
