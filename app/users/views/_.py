from rest_framework.mixins import ListModelMixin

from app.users.filters import UsersFilterSet
from app.users.models import User
from app.users.views import BaseAuthView


class UsersView(ListModelMixin, BaseAuthView):
    queryset = User.objects.all()
    filterset_class = UsersFilterSet
    
    def get(self, request):
        return self.list(request)
    
    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user)
