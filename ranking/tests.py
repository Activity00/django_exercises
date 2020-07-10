import time

from django.test import TestCase
from django_redis import get_redis_connection

from ranking import const

conn = get_redis_connection()
conn.delete(const.RK_RANKING)


class RankingTest(TestCase):
    def setUp(self):
        self.own_device = '客户端5'
        self.own_score = 3453452
        self.player_info = [
            {'ranking': 1, 'device_id': '客户端1', 'score': 9999999},
            {'ranking': 2, 'device_id': '客户端2', 'score': 9500112},
            {'ranking': 3, 'device_id': '客户端3', 'score': 9233333},
            {'ranking': 4, 'device_id': '客户端4', 'score': 5445444},
            {'ranking': 5, 'device_id': '客户端5', 'score': 3453452},
            {'ranking': 6, 'device_id': '客户端6', 'score': 2342342},
            {'ranking': 7, 'device_id': '客户端8', 'score': 66666},
            {'ranking': 8, 'device_id': '客户端7', 'score': 66666},
            {'ranking': 9, 'device_id': '客户端9', 'score': 76},
            {'ranking': 10, 'device_id': '客户端10', 'score': 75},
        ]

    def test_get(self):
        self._post()
        response = self.client.get('/api/ranking/', data={'device_id': self.own_device})
        self.assertEqual(200, response.status_code)
        self.player_info.append({'ranking': 5, 'device_id': '客户端5', 'score': 3453452})
        self.assertListEqual(self.player_info, response.data['data'])

    def _post(self):
        for info in self.player_info:
            device_id, score = info['device_id'], info['score']
            params = {'device_id': device_id, 'score': score}
            response = self.client.post('/api/ranking/', data=params)
            self.assertEqual(200, response.status_code)
