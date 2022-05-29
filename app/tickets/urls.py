from django.urls import path

from .views import *

urlpatterns = [
    path('sessions/', TicketsSessionsView.as_view()),
    path('sessions/<str:session_id>/', TicketsSessions_SessionId_View.as_view()),
]
