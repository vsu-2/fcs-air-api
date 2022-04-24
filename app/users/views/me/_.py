from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from app.users.serializers.me import GetUsersMeSerializer, PatchUsersMeSerializer
from app.users.views.base import BaseAuthView


class UsersMeView(RetrieveModelMixin, UpdateModelMixin, BaseAuthView):
    serializer_class_map = {'get': GetUsersMeSerializer, 'patch': PatchUsersMeSerializer}
    
    def get(self, request):
        return self.retrieve(request)
    
    def patch(self, request):
        return self.partial_update(request)
    
    def get_object(self):
        return self.request.user
