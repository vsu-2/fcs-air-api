from app.base.filters.filtersets.base import BaseFilterSet
from app.users.models import User


class UsersFilterSet(BaseFilterSet):
    class Meta:
        model = User
        fields = {'first_name': ['icontains'], 'last_name': ['icontains']}
