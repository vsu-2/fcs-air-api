from rest_framework import serializers

from app.geo.models import Airport, City, Country


class _GETGeoCitiesCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'title', 'code']


class _GETGeoCitiesAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'title', 'code']


class GETGeoCitiesSerializer(serializers.ModelSerializer):
    country = _GETGeoCitiesCountrySerializer()
    airports = _GETGeoCitiesAirportSerializer(many=True, source='airport_set')
    
    class Meta:
        model = City
        fields = ['id', 'title', 'code', 'country', 'airports']
