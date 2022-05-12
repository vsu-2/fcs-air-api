from rest_framework.mixins import ListModelMixin

from app.geo.filters.cities import GeoCitiesFilterSet
from app.geo.models import City
from app.base.views.base import BaseView


class GeoCitiesView(ListModelMixin, BaseView):
    queryset = City.objects.distinct().prefetch_related('country', 'airports')
    filterset_class = GeoCitiesFilterSet
    
    def get(self, request, **_):
        return self.list(request)
