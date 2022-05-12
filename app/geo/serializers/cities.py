from rest_framework import serializers

from app.geo.models import Airport, City, Country


class _GET_GeoCities__CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'title', 'code']


class _GET_GeoCities__AirportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'title', 'code']


class GET_GeoCitiesSerializer(serializers.ModelSerializer):
    country = _GET_GeoCities__CountrySerializer()
    airports = _GET_GeoCities__AirportsSerializer(many=True)
    
    class Meta:
        model = City
        fields = ['id', 'title', 'code', 'country', 'airports']
