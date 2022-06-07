from rest_framework import serializers

from app.base.serializers.base import BaseSerializer


class GET_TicketsSessionsDetailOffersDetailLinkSerializer(BaseSerializer):
    link = serializers.CharField(read_only=True)
