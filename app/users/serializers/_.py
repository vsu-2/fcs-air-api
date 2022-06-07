from rest_framework import serializers

from app.users.models import User


class GET_UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
