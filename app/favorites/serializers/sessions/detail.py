from rest_framework import serializers

from app.base.serializers.base import BaseSerializer
from app.favorites.models import Favorite


class GET_FavoritesSessionsDetailSerializer(BaseSerializer):
    is_favorite = serializers.BooleanField(read_only=True)


class POST_FavoritesSessionsDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    query = serializers.HiddenField(default=None)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'query']
    
    def create(self, validated_data):
        validated_data['query'] = self.context['view'].session.query
        return Favorite.objects.get_or_create(**validated_data)
