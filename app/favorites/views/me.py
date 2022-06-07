from rest_framework.mixins import ListModelMixin

from app.air.models import Query
from app.users.views import BaseAuthView


class FavoritesMeView(ListModelMixin, BaseAuthView):
    queryset = Query.objects.all()
    
    def get(self, request):
        return self.list(request)
    
    def get_queryset(self):
        return super().get_queryset().filter(favorites__user=self.request.user)
