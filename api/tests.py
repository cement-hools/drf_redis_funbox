from unittest.mock import patch

from django.test import TestCase
from fakeredis import FakeStrictRedis
from rest_framework import status
from rest_framework.reverse import reverse


class TestViews(TestCase):

    def setUp(self):
        self.redis_patcher = patch('api.views.redis_instance',
                                   FakeStrictRedis(decode_responses=True))
        self.redis = self.redis_patcher.start()

        self.client = self.client_class()

        self.start_domains = {
            'stepik.org': '1631497327',
            'google.com': '1631497328',
            'youtube.com': '1631497329',
        }
        for key, value in self.start_domains.items():
            self.redis.set(key, value)

    def test_visited_all_domains(self):
        """Получение всех доменов в базе."""
        url = reverse('visited_domains')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Статус ответа')

        self.assertIn('domains', response.data, 'ключ не содержится в выдаче')
        self.assertIn('status', response.data, 'ключ не содержится в выдаче')

        start_domains_list = list(self.start_domains.keys())
        self.assertEqual(start_domains_list, response.data['domains'],
                         'стартовый список доменов не совпадает с выдачей')

    def test_visited_domains_in_time_diapason(self):
        """Получение всех доменов в диапазоне времени."""
        url = reverse('visited_domains')
        data = {
            'from': '1631497328',
            'to': '1631497329'
        }

        response = self.client.get(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Статус ответа')

        self.assertIn('domains', response.data, 'ключ не содержится в выдаче')
        self.assertIn('status', response.data, 'ключ не содержится в выдаче')

        domains_list = ['google.com', 'youtube.com']
        self.assertEqual(domains_list, response.data['domains'],
                         'стартовый список доменов не совпадает с выдачей')

    def test_visited_domains_in_time_diapason_from(self):
        """Получение всех доменов в диапазоне времени c параметром from."""
        url = reverse('visited_domains')
        data = {
            'from': '1631497329',
        }

        response = self.client.get(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Статус ответа')

        self.assertIn('domains', response.data, 'ключ не содержится в выдаче')
        self.assertIn('status', response.data, 'ключ не содержится в выдаче')

        domains_list = ['youtube.com']
        self.assertEqual(domains_list, response.data['domains'],
                         'стартовый список доменов не совпадает с выдачей')

    def test_visited_domains_in_time_diapason_to(self):
        """Получение всех доменов в диапазоне времени c параметром to."""
        url = reverse('visited_domains')
        data = {
            'to': '1631497328',
        }

        response = self.client.get(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         'Статус ответа')

        self.assertIn('domains', response.data, 'ключ не содержится в выдаче')
        self.assertIn('status', response.data, 'ключ не содержится в выдаче')

        domains_list = ['stepik.org', 'google.com']
        self.assertEqual(domains_list, response.data['domains'],
                         'стартовый список доменов не совпадает с выдачей')

    def test_visited_domains_in_time_diapason_invalid_data(self):
        """Невалидные GET параметры."""
        url = reverse('visited_domains')
        data = {
            'from': 'october',
            'to': 'winter'
        }
        response = self.client.get(url, data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         'Статус ответа')

        self.assertIn('status', response.data, 'ключ не содержится в выдаче')
        self.assertEqual('bad GET parameter', response.data['status'],
                         'текст ответа')

    def test_visited_links(self):
        """Загрузка посещений."""
        data = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-ex-edit",
            ]
        }
        url = reverse('visited_links')
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Статус ответа')

        keys_count = len(self.redis.keys('*'))
        self.assertEqual(6, keys_count, 'неверное количество записей в базе')
        result_list = self.redis.keys('*')
        adding_list = ['ya.ru', 'funbox.ru', 'stackoverflow.com']
        occurrence = set(adding_list).issubset(result_list)
        self.assertTrue(occurrence, 'список запроса не входит в список БД')

    def test_visited_links_invalid_data(self):
        """Загрузка посещений с неверными данными."""
        data = {
            "domains": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-ex-edit",
            ]
        }
        url = reverse('visited_links')
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         'Статус ответа')

        self.assertIn('status', response.data, 'ключ не содержится в выдаче')
        self.assertEqual('fail', response.data['status'],
                         'текст ответа')
