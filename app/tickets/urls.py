from django.urls import path

from .views import *

urlpatterns = [
    path('sessions/', TicketsSessionsView.as_view()),
    path('sessions/<str:id>/tickets/', TicketsSessionsDetailTicketsView.as_view()),
    path('sessions/<str:id>/filters/', TicketsSessionsDetailFiltersView.as_view()),
]
