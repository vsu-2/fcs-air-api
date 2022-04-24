from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from app.users.models import User
from app.base.exceptions import APIWarning
from app.base.schemas.mixins import SerializerSchemaMixin


class _EmailUniqueValidator(UniqueValidator):
    def __call__(self, value, serializer_field):
        try:
            super().__call__(value, serializer_field)
        except ValidationError:
            raise PostUsersRegisterSerializer.WARNINGS[409]


class PostUsersRegisterSerializer(SerializerSchemaMixin, serializers.ModelSerializer):
    WARNINGS = {
        409: APIWarning('User с таким email уже существует', 409, 'register_email_unique')
    }
    
    class Meta:
        model = User
        extra_kwargs = {
            'email': {
                'validators': [_EmailUniqueValidator(queryset=User.objects.all())],
                'write_only': True
            }, 'password': {'write_only': True}, 'first_name': {'write_only': True},
            'last_name': {'write_only': True, 'required': False}, 'id': {}
        }
        fields = list(extra_kwargs.keys())
    
    def validate(self, attrs):
        validate_password(attrs['password'], User(**attrs))
        return attrs
    
    def create(self, validated_data):
        self.instance = User.objects.create_user(**validated_data)
        return self.instance


class PostUsersRegisterResendSerializer(serializers.ModelSerializer):
    WARNINGS = {
        404: APIWarning(
            'Пользователь с таким email не регистрировался', 404,
            'register_resend_email_not_found'
        ),
        409: APIWarning(
            'Пользователь уже верифицирован', 409, 'register_resend_already_verified'
        )
    }
    
    class Meta:
        model = User
        extra_kwargs = {'email': {'write_only': True, 'validators': []}}
        fields = list(extra_kwargs.keys())
    
    def validate(self, attrs):
        try:
            self.instance = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise self.WARNINGS[404]
        if self.instance.is_active:
            raise self.WARNINGS[409]
        return attrs
