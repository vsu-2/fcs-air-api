from rest_framework import serializers

from app.geo.models import *
from app.tickets.models import *


class GET_TicketsSessions_SessionId__BestOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'gate_id', 'title', 'price']


class GET_TicketsSessions_SessionId__Trips__Segments__Departure_Arrival__CitySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = City
        fields = ['id', 'code', 'title']


class GET_TicketsSessions_SessionId__Trips__Segments__Departure_ArrivalSerializer(
    serializers.ModelSerializer
):
    city = \
        GET_TicketsSessions_SessionId__Trips__Segments__Departure_Arrival__CitySerializer(
        )
    
    class Meta:
        model = Airport
        fields = ['id', 'code', 'title', 'city']


class GET_TicketsSessions_SessionId__Trips__Segments__MarketingAirlineSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Airline
        fields = ['id', 'code', 'title']


class GET_TicketsSessions_SessionId__Trips__SegmentsSerializer(
    serializers.ModelSerializer
):
    departure = \
        GET_TicketsSessions_SessionId__Trips__Segments__Departure_ArrivalSerializer()
    arrival = \
        GET_TicketsSessions_SessionId__Trips__Segments__Departure_ArrivalSerializer()
    marketing_airline = \
        GET_TicketsSessions_SessionId__Trips__Segments__MarketingAirlineSerializer()
    
    class Meta:
        model = Segment
        fields = [
            'id', 'departure', 'arrival', 'departure_time', 'arrival_time', 'duration',
            'marketing_airline', 'flight'
        ]


class GET_TicketsSessions_SessionId__TripsSerializer(serializers.ModelSerializer):
    segments = GET_TicketsSessions_SessionId__Trips__SegmentsSerializer(many=True)
    
    class Meta:
        model = Trip
        fields = ['start_time', 'end_time', 'segments']


class GET_TicketsSessions_SessionId_Serializer(serializers.ModelSerializer):
    best_offer = GET_TicketsSessions_SessionId__BestOfferSerializer()
    trips = GET_TicketsSessions_SessionId__TripsSerializer(many=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'best_offer', 'trips']
