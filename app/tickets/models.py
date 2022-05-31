from django.db import models

from app.base.models.base import AbstractModel


class Ticket(AbstractModel):
    query = models.ForeignKey(
        'air.Query', on_delete=models.PROTECT, related_name='tickets'
    )
    best_offer = models.ForeignKey(
        'tickets.Offer', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tickets_by_best_offer'
    )
    sign = models.TextField()
    travel_time = models.DurationField(null=True, blank=True)


class Trip(AbstractModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='trips')
    origin = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='trips_by_origin'
    )
    destination = models.ForeignKey(
        'geo.City', on_delete=models.CASCADE, related_name='trips_by_destination'
    )
    number = models.PositiveSmallIntegerField(
        help_text='Порядковый номер в сложном маршруте'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()


class Offer(AbstractModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='offers')
    gate_id = models.IntegerField()
    title = models.TextField()
    price = models.FloatField()
    url = models.IntegerField()
    
    class Meta(AbstractModel.Meta):
        unique_together = ('ticket', 'gate_id')


class Segment(AbstractModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='segments')
    departure = models.ForeignKey(
        'geo.Airport', on_delete=models.CASCADE, related_name='segments_by_departure'
    )
    arrival = models.ForeignKey(
        'geo.Airport', on_delete=models.CASCADE, related_name='segments_by_arrival'
    )
    marketing_airline = models.ForeignKey(
        'geo.Airline', on_delete=models.CASCADE, related_name='segments'
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    flight = models.TextField()


class About(AbstractModel):
    segment = models.OneToOneField(Segment, on_delete=models.CASCADE)
    airline = models.ForeignKey(
        'geo.Airline', on_delete=models.CASCADE, related_name='abouts'
    )
    aircraft = models.TextField(null=True, blank=True)
    food = models.BooleanField(null=True, blank=True)
    entertainment = models.BooleanField(null=True, blank=True)
    alcohol = models.BooleanField(null=True, blank=True)
    beverage = models.BooleanField(null=True, blank=True)
    power = models.BooleanField(null=True, blank=True)
    wifi = models.BooleanField(null=True, blank=True)
