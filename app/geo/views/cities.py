from rest_framework.mixins import ListModelMixin

from app.geo.filters.cities import GeoCitiesFilterSet
from app.geo.models import City
from app.geo.serializers.cities import GETGeoCitiesSerializer
from app.base.views.base import BaseView


class GeoCitiesView(ListModelMixin, BaseView):
    serializer_class_map = {'get': GETGeoCitiesSerializer}
    queryset = City.objects.distinct().prefetch_related('country', 'airport_set')
    filterset_class = GeoCitiesFilterSet
    
    def get(self, request, **_):
        return self.list(request)
