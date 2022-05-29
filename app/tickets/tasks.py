from celery import shared_task

from app.tickets.components.services.search import SearchTicketsService
from app.tickets.components.services.session import TicketsSessionService


@shared_task
def search_tickets(session_id):
    session = TicketsSessionService(session_id)
    service = SearchTicketsService(session)
    service.search(session.query)
