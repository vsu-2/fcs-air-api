from rest_framework import serializers

from app.users.models import User
from app.users.models.choices import UserType


class GetUsersMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ro = {'read_only': True}
        extra_kwargs = {
            'first_name': {}, 'last_name': {'allow_null': True}, 'email': ro,
            'type': {'read_only': True, 'help_text': UserType.help_text}
        }
        fields = list(extra_kwargs.keys())


PatchUsersMeSerializer = GetUsersMeSerializer
