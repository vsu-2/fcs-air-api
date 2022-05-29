from collections import OrderedDict

from rest_framework.response import Response

from app.base.paginations.base import BasePagination


class TicketsSessions_SessionId_Pagination(BasePagination):
    def get_paginated_response(self, data, in_progress=False):
        return Response(
            OrderedDict(
                [
                    ('in_progress', in_progress),
                    ('count', self.page.paginator.count),
                    ('results', data)
                ]
            )
        )
    
    def get_paginated_response_schema(self, schema):
        response_schema = super().get_paginated_response_schema(schema)
        in_progress_schema = {'in_progress': {'type': 'boolean', 'example': True}}
        response_schema['properties'] = in_progress_schema | response_schema['properties']
        return response_schema
