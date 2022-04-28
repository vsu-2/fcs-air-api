import factory
from django.contrib.auth.hashers import make_password

from app.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    raw_password: str
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_active = True
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raw_password = kwargs['password']
        obj = super(UserFactory, cls)._create(
            model_class, *args, **kwargs | {'password': make_password(raw_password)}
        )
        obj.raw_password = raw_password
        return obj
