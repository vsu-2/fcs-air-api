from app.base.controllers.base import BaseController
from app.favorites.models import Favorite
from app.favorites.views.sessions.detail import FavoritesSessionsDetailView


class GET_FavoritesSessionsDetailController(BaseController):
    view: FavoritesSessionsDetailView
    
    def control(self, data):
        return {
            'is_favorite': Favorite.objects.filter(
                user=self.view.request.user, query=self.view.session.query
            ).exists()
        }
