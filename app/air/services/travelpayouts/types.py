import datetime
from typing import Literal, TypedDict


class TripType(TypedDict):
    origin: str
    destination: str
    date: datetime.date


class _NameTranslationsType(TypedDict):
    en: str


class _EN_DE_CasesType(TypedDict):
    su: str


class _RU_CasesType(TypedDict):
    da: str
    pr: str
    ro: str
    su: str
    tv: str
    vi: str


_CasesType = _EN_DE_CasesType | _RU_CasesType


class CountryType(TypedDict):
    code: str
    name: str
    currency: str
    name_translations: _NameTranslationsType
    cases: _CasesType


class _CoordinatesType(TypedDict):
    lon: float
    lat: float


class CityType(TypedDict):
    code: str
    country_code: str
    coordinates: _CoordinatesType
    name: str
    time_zone: str
    name_translations: _NameTranslationsType
    cases: _CasesType


_NameType = str | None


class AirportType(TypedDict):
    code: str
    city_code: str
    country_code: str
    name_translations: _NameTranslationsType
    time_zone: str
    flightable: bool
    coordinates: _CoordinatesType
    name: _NameType
    iata_type: Literal[
        'airport', 'railway', '', 'heliport', 'bus', 'military', 'seaplane', 'harbour',
        'airline'
    ]


class AirlineType(TypedDict):
    code: str
    name: str
    name_translations: _NameTranslationsType


class WhereamiType(TypedDict):
    iata: str
    name: str
    country_name: str
    coordinates: _CoordinatesType


class CurrencyType(TypedDict):
    usd: float
    eur: float
    ...


class CalendarType(TypedDict):
    price: int
    departure_at: str
    origin_airport: str
    destination_airport: str
    airline: str
    duration: str
    link: str


class GetSpecialOffersResult(TypedDict):
    price: int
    departure_at: str
