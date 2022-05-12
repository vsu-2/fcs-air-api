from django.db.models import Q
from django_filters import filters

from app.geo.models import City
from app.base.filters.filtersets.base import BaseFilterSet


class GeoCitiesFilterSet(BaseFilterSet):
    title__icontains = filters.CharFilter(
        method='filter_title__icontains', label='Title начинается'
    )
    
    class Meta:
        model = City
        fields = {}
        filter_overrides = {'title': ['icontains']}
    
    @staticmethod
    def filter_title__icontains(queryset, name, value):
        _name = f'{name.split("__")[0]}__{name.split("__")[1]}'
        return queryset.filter(Q(**{_name: value}) | Q(**{f'airports__{_name}': value}))
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if last_name := self.data.get('title__icontains'):
            last_name = last_name.lower()
            queryset = list(queryset)
            queryset.sort(
                key=lambda r: i if (i := r.title.lower().find(last_name)) >= 0 else float(
                    'inf'
                )
            )
        return queryset
