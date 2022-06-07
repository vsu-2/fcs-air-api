from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin

from app.base.utils.common import response_204
from app.favorites.models import Favorite
from app.tickets.views.sessions.detail.base import BaseTicketsSessionsDetailView
from app.users.permissions import IsAuthenticatedPermission
from app.users.views import BaseAuthView


class FavoritesSessionsDetailView(
    CreateModelMixin, DestroyModelMixin, BaseTicketsSessionsDetailView
):
    permission_classes = [IsAuthenticatedPermission]
    queryset = Favorite.objects.all()
    
    def get(self, request, **_):
        return self.handle()

    @response_204
    def post(self, request, **_):
        self.create(request)

    def delete(self, request, **_):
        return self.destroy(request)
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return get_object_or_404(
            queryset, user=self.request.user, query=self.session.query
        )
    
    _to_auth_schema = getattr(BaseAuthView, '_to_auth_schema')
    _to_schema = getattr(BaseAuthView, '_to_schema')
