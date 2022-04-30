from django.db import models

from app.base.models.base import AbstractModel


class Ticket(AbstractModel):
    sign = models.TextField(unique=True)
    best_offer = models.ForeignKey(
        'tickets.Offer', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ticket_by_best_offer'
    )
    query = models.ForeignKey('air.Query', on_delete=models.PROTECT)


class Trip(AbstractModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    origin = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='trip_by_origin'
    )
    destination = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='trip_by_destination'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    transfer_time = models.IntegerField()
    transfer_airports = models.ManyToManyField(
        'geo.Airport', related_name='trip_by_transfer_airports'
    )


class Offer(AbstractModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    gate_id = models.IntegerField()
    title = models.TextField()
    price = models.FloatField()
    url = models.IntegerField()
    
    class Meta(AbstractModel.Meta):
        unique_together = ('ticket', 'gate_id')


class Segment(AbstractModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    departure = models.ForeignKey(
        'geo.Airport', on_delete=models.CASCADE, related_name='segment_by_departure'
    )
    arrival = models.ForeignKey(
        'geo.Airport', on_delete=models.CASCADE, related_name='segment_by_arrival'
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    marketing_airline = models.ForeignKey('geo.Airline', on_delete=models.CASCADE)
    flight = models.TextField()
    handbags_weight = models.PositiveSmallIntegerField(null=True, blank=True)
    baggage_weight = models.PositiveSmallIntegerField(null=True, blank=True)


class About(AbstractModel):
    segment = models.OneToOneField(Segment, on_delete=models.CASCADE)
    airline = models.ForeignKey('geo.Airline', on_delete=models.CASCADE)
    aircraft = models.TextField(null=True, blank=True)
    food = models.BooleanField(null=True, blank=True)
    entertainment = models.BooleanField(null=True, blank=True)
    alcohol = models.BooleanField(null=True, blank=True)
    beverage = models.BooleanField(null=True, blank=True)
    power = models.BooleanField(null=True, blank=True)
    wifi = models.BooleanField(null=True, blank=True)
