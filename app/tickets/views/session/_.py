from app.base.views.base import BaseView


class TicketsSessionView(BaseView):
    def post(self, _):
        return self.handle()
