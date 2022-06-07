from django.urls import path

from .views import *

urlpatterns = [
    path('sessions/<str:id>/', FavoritesSessionsDetailView.as_view()),
    path('me/', FavoritesMeView.as_view()),
]
