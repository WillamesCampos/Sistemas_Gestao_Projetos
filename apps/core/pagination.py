from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):

    invalid_page_message = ('Página inválida')
    page_query_param = 'pagina'

    def get_paginated_response(self, data):
        return Response({
            'pagina_atual': self.get_page_number(
                self.request,
                PageNumberPagination
            ),
            'links': {
                'proximo': self.get_next_link(),
                'anterior': self.get_previous_link()
            },
            'quantidade': self.page.paginator.count,
            'resultados': data
        })