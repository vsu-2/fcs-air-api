from dataclasses import dataclass
import datetime
from typing import List

from app.air.models import FlightClass
from app.base.entities.base import BaseEntity
from app.geo.models import City


@dataclass
class QueryTripEntity(BaseEntity):
    origin: City
    destination: City
    date: datetime.date


@dataclass
class QueryEntity(BaseEntity):
    trips: List[QueryTripEntity]
    passengers: int
    flight_class: FlightClass
