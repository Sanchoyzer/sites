import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import History, SearchArea, User
from ..serializers import HistorySerializer, SearchAreaSerializer


client = Client()


class SearchAreaGetTest(TestCase):
    def setUp(self):
        SearchArea.objects.create(name='area_1')
        SearchArea.objects.create(name='area_2')

    def test_get_search_area_list(self):
        response = client.get(reverse('geobot:search-area'))

        search_areas = SearchArea.objects.all()
        serializer = SearchAreaSerializer(search_areas, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class HistoryGetTest(TestCase):
    def setUp(self):
        u1 = User.objects.create(t_user_id=10)
        u2 = User.objects.create(t_user_id=20)
        History.objects.create(request='1', result='2', user=u1)
        History.objects.create(request='3', result='4', user=u1)
        History.objects.create(request='5', result='6', user=u2)

    def test_get_history_list(self):
        response = client.get(reverse('geobot:history'))
        histories = History.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), histories.count())

    def test_get_history_list_filter(self):
        users = User.objects.all()
        for user in users:
            t_user_id = user.t_user_id
            response = client.get(reverse('geobot:history'), data={'user': t_user_id})
            histories = History.objects.filter(user__t_user_id=t_user_id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('count'), histories.count())


class HistoryPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(t_user_id=10)
        self.data = {
            'request': '1',
            'result': '2',
            'user': str(self.user.t_user_id),
        }

    def test_post_history(self):
        self.assertEqual(History.objects.count(), 0)

        response = client.post(
            reverse('geobot:history'),
            data=json.dumps(self.data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(History.objects.count(), 1)
        self.assertEqual(response.data, self.data)
