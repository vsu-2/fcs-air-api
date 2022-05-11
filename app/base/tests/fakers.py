from typing import Callable, Final

from factory import Faker as _FactoryFaker
from faker import Faker as _Faker


class SubFaker(_Faker):
    first_name: Callable[..., str]
    last_name: Callable[..., str]
    password: Callable[..., str]


class Faker(_FactoryFaker):
    @classmethod
    def _get_faker(cls, locale=None):
        if locale is None:
            locale = cls._DEFAULT_LOCALE

        if locale not in cls._FAKER_REGISTRY:
            sub_faker = SubFaker(locale=locale).unique
            cls._FAKER_REGISTRY[locale] = sub_faker

        return cls._FAKER_REGISTRY[locale]


fake: Final[SubFaker] = SubFaker()
