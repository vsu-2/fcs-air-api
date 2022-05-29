from app.base.views.base import BaseView


class TicketsSessionsView(BaseView):
    def post(self, _):
        return self.handle()
