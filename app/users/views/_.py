from app.users.models import User
from app.users.views import BaseAuthView


class UsersView(BaseAuthView):
    queryset = User.objects.all()
    
    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user)
