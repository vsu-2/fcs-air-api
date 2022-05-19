from django.urls import path

from .views import *

urlpatterns = [
    path('session/', TicketsSessionView.as_view()),
]
