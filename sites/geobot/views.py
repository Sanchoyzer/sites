from rest_framework import generics, pagination

from .models import History, SearchArea
from .serializers import HistorySerializer, SearchAreaSerializer


class HistoryPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchAreaView(generics.ListAPIView):
    queryset = SearchArea.objects.all()
    serializer_class = SearchAreaSerializer


class HistoryView(generics.ListCreateAPIView):
    serializer_class = HistorySerializer
    pagination_class = HistoryPagination

    def get_queryset(self):
        t_user = self.request.query_params.get('user')
        queryset = History.objects.all()
        if t_user:
            queryset = queryset.filter(user__t_user_id=t_user)
        return queryset.order_by('-date')
