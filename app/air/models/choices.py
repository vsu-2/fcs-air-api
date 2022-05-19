from app.base.models.choices.base import TextChoices


class FlightClass(TextChoices):
    ECONOMY = 'Y', 'Эконом'
    BUSINESS = 'C', 'Бизнес'
