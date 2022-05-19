from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from rest_framework import serializers

from app.air.models import FlightClass, Query, QueryTrip


class _POST_TicketsSession__TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryTrip
        wo = {'write_only': True}
        extra_kwargs = {
            'origin': wo, 'destination': wo, 'date': wo | {
                'validators': [
                    MinValueValidator(lambda: timezone.now().date()),
                    MaxValueValidator(lambda: timezone.now().date() + timedelta(days=330))
                ]
            }
        }
        fields = list(extra_kwargs.keys())


class POST_TicketsSessionSerializer(serializers.ModelSerializer):
    trips = _POST_TicketsSession__TripsSerializer(many=True, write_only=True)
    passengers = serializers.IntegerField(write_only=True, min_value=1, default=1)
    flight_class = serializers.ChoiceField(
        choices=FlightClass.choices, help_text=FlightClass.help_text,
        write_only=True, default=FlightClass.ECONOMY
    )
    session_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Query
        fields = ['trips', 'passengers', 'flight_class', 'session_id']
