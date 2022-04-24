from rest_framework import serializers

from app.users.models import User
from app.base.exceptions import APIWarning
from app.base.schemas.mixins import SerializerSchemaMixin


class PostUsersPasswordSerializer(serializers.ModelSerializer):
    WARNINGS = {
        404: APIWarning(
            'Пользователя с таким email не существует', 404,
            'password_forgot_email_not_found'
        )
    }
    
    class Meta:
        model = User
        extra_kwargs = {'email': {'validators': [], 'write_only': True}}
        fields = list(extra_kwargs.keys())
    
    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise self.WARNINGS[404]
        return attrs


class PutUsersPasswordSerializer(SerializerSchemaMixin, serializers.ModelSerializer):
    WARNINGS = {408: APIWarning('Сессия просрочена', 408, 'password_session_time_out')}
    
    session = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        extra_kwargs = {'session': {}, 'password': {'write_only': True}, 'token': {}}
        fields = list(extra_kwargs.keys())
