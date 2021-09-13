from unittest.mock import patch

from django.test import TestCase
from fakeredis import FakeStrictRedis
from rest_framework import status
from rest_framework.reverse import reverse


class TestViews(TestCase):
    redis_patcher = patch('api.views.redis_instance', FakeStrictRedis())

    def setUp(self):
        self.redis = self.redis_patcher.start()

        self.client = self.client_class()

        start_domains = {
            'stepik.org': '1631497327',
            'google.com': '1631497328',
            'youtube.com': '1631497329',
        }
        for key, value in start_domains.items():
            self.redis.set(key, value)

    def tearDown(self):
        self.redis.flushdb()
        self.redis_patcher.stop()

    def test_visited_domains(self):
        for key in self.redis.keys('*'):
            print(key, self.redis.get(key))

    def test_visited_links(self):
        data = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-ex-editor"
            ]
        }
        url = reverse('visited_links')
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code,
                         'Статус ответа')
        keys_count = len(self.redis.keys('*'))
        self.assertEqual(6, keys_count, 'неверное количество записей в базе')

        for key in self.redis.keys('*'):
            print(key, self.redis.get(key))
