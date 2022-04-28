from django.contrib.auth import authenticate
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app.users.models import User
from app.users.models.choices import UserType
from app.users.services.auth import AuthService
from app.base.exceptions import APIWarning
from app.base.schemas.mixins import SerializerSchemaMixin


class PostUsersTokenSerializer(SerializerSchemaMixin, serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    
    WARNINGS = {
        401: APIWarning('Неверный пароль', 401, 'invalid_password'),
        404: APIWarning(
            'Пользователя с таким email не существует', 404, 'email_not_found'
        ),
        406: APIWarning('Пользователь не верифицирован', 406, 'not_verified'),
        410: APIWarning('Пользователь забанен', 410, 'banned')
    }
    
    class Meta:
        model = User
        extra_kwargs = {
            'email': {'write_only': True, 'validators': []},
            'password': {'write_only': True}, 'token': {}
        }
        fields = list(extra_kwargs.keys())
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_token(self, user):
        return AuthService(self.context['request'], user).login()
    
    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        
        user: User = authenticate(
            request=self.context.get('request'), email=email, password=password
        )
        if user is None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise self.WARNINGS[404]
            if not user.check_password(password):
                raise self.WARNINGS[401]
            if user.type == UserType.BANNED:
                raise self.WARNINGS[410]
            if not user.is_active:
                raise self.WARNINGS[406]
        self.instance = user
        return attrs
