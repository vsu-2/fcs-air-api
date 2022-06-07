from rest_framework import serializers

from app.air.models import Query, QueryTrip
from app.geo.models import City


class _GET_FavoritesMe__Trips__Origin_DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'code', 'title']


class _GET_FavoritesMe__TripsSerializer(serializers.ModelSerializer):
    origin = _GET_FavoritesMe__Trips__Origin_DestinationSerializer()
    destination = _GET_FavoritesMe__Trips__Origin_DestinationSerializer()
    
    class Meta:
        model = QueryTrip
        fields = ['id', 'origin', 'destination', 'date']


class GET_FavoritesMeSerializer(serializers.ModelSerializer):
    trips = _GET_FavoritesMe__TripsSerializer(many=True)
    
    class Meta:
        model = Query
        fields = ['id', 'passengers', 'flight_class', 'trips']
