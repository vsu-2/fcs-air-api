from celery.result import AsyncResult

from app.base.exceptions import APIWarning, CriticalError
from app.base.logs import debug
from app.base.schemas.mixins import ViewSchemaMixin
from app.base.views.base import BaseView
from app.tickets.components.services.session import TicketsSessionService


class BaseTicketsSessionsDetailView(ViewSchemaMixin, BaseView):
    WARNINGS = {
        408: APIWarning('Время жизни сессии закончилось', 408, 'tickets_session_timeout')
    }
    
    @property
    def session(self) -> TicketsSessionService:
        session = TicketsSessionService(self.kwargs['id'])
        if session.task_id is None:
            raise self.WARNINGS[408]
        return session
    
    @property
    def is_in_progress(self) -> bool:
        task_id = self.session.task_id
        result = AsyncResult(task_id)
        result_status = result.status
        debug(f'air ticket session {task_id} status: {result_status}')
        if result_status == 'FAILURE':
            raise CriticalError(
                f'ticket session {task_id} traceback:\n{result.traceback}'
            )
        return result_status != 'SUCCESS'
