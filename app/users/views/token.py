from rest_framework.response import Response

from app.base.utils.common import response_204
from app.base.views.base import BaseView
from app.users.permissions import IsAuthenticatedPermission
from app.users.serializers.token import PostUsersTokenSerializer
from app.users.services.auth import AuthService


class UsersTokenView(BaseView):
    serializer_class_map = {'post': PostUsersTokenSerializer}
    permission_classes_map = {'delete': [IsAuthenticatedPermission]}
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=201)
    
    @response_204
    def delete(self, request):
        AuthService(request).logout()
