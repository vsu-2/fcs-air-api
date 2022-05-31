from rest_framework import serializers

from app.base.serializers.base import BaseSerializer
from app.geo.models import *
from app.tickets.models import Offer


class _GET_TicketsSessionsDetailFilters__TravelTimeRangeSerializer(BaseSerializer):
    min = serializers.DurationField(help_text='type: timedelta in seconds')
    max = serializers.DurationField(help_text='type: timedelta in seconds')


class _GET_TicketsSessionsDetailFilters__AirlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'code', 'title']


class _GET_TicketsSessionsDetailFilters__AirportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'code', 'title']


class _GET_TicketsSessionsDetailFilters__OffersSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    
    class Meta:
        model = Offer
        fields = ['gate_id', 'title', 'price']


class GET_TicketsSessionsDetailFiltersSerializer(BaseSerializer):
    in_progress = serializers.BooleanField(read_only=True)
    transfers = serializers.ListField(child=serializers.IntegerField(), read_only=True)
    travel_time_range = _GET_TicketsSessionsDetailFilters__TravelTimeRangeSerializer(
        read_only=True
    )
    airlines = _GET_TicketsSessionsDetailFilters__AirlinesSerializer(
        many=True, read_only=True
    )
    airports = _GET_TicketsSessionsDetailFilters__AirportsSerializer(
        many=True, read_only=True
    )
    offers = _GET_TicketsSessionsDetailFilters__OffersSerializer(
        many=True, read_only=True
    )
