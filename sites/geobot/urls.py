from django.urls import path

from .views import HistoryView, SearchAreaView


app_name = 'geobot'
urlpatterns = [
    path('search_area/', SearchAreaView.as_view(), name='search-area'),
    path('history/', HistoryView.as_view(), name='history'),
]
