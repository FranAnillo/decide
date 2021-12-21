from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_mayoria_absoluta1(self):
        data = {
            'type': 'MAYORIA_ABSOLUTA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
            ]
        }

        expected_result = [
                { 'option': 'Option 1', 'number': 1, 'votes': 2, 'postproc': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_mayoria_absoluta2(self):
        data = {
            'type': 'MAYORIA_ABSOLUTA',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100},
                {'option': 'Option 2', 'number': 2, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votes': 6},
                {'option': 'Option 4', 'number': 4, 'votes': 4},
                {'option': 'Option 5', 'number': 5, 'votes': 10},
                {'option': 'Option 6', 'number': 6, 'votes': 2},
                {'option': 'Option 7', 'number': 7, 'votes': 6},
            ]
        }

        expected_result = [
                {'option': 'Option 1', 'number': 1, 'votes': 100, 'postproc': 1},
                {'option': 'Option 5', 'number': 5, 'votes': 10, 'postproc': 0},
                {'option': 'Option 3', 'number': 3, 'votes': 6, 'postproc': 0},
                {'option': 'Option 7', 'number': 7, 'votes': 6, 'postproc': 0},
                {'option': 'Option 4', 'number': 4, 'votes': 4, 'postproc': 0},
                {'option': 'Option 6', 'number': 6, 'votes': 2, 'postproc': 0},
                {'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0},

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_mayoria_absoluta3(self):
        data = {
            'type': 'MAYORIA_ABSOLUTA',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 74},
                {'option': 'Option 2', 'number': 2, 'votes': 12},
                {'option': 'Option 3', 'number': 3, 'votes': 89},
                {'option': 'Option 4', 'number': 4, 'votes': 27},
                {'option': 'Option 5', 'number': 5, 'votes': 46},
                {'option': 'Option 6', 'number': 6, 'votes': 21},
                {'option': 'Option 7', 'number': 7, 'votes': 17},
                {'option': 'Option 8', 'number': 8, 'votes': 41},
            ]
        }

        expected_result = [
                {'option': 'Option 3', 'number': 3, 'votes': 89, 'postproc': 0},
                {'option': 'Option 1', 'number': 1, 'votes': 74, 'postproc': 0},
                {'option': 'Option 5', 'number': 5, 'votes': 46, 'postproc': 0},
                {'option': 'Option 8', 'number': 8, 'votes': 41, 'postproc': 0},
                {'option': 'Option 4', 'number': 4, 'votes': 27, 'postproc': 0},
                {'option': 'Option 6', 'number': 6, 'votes': 21, 'postproc': 0},
                {'option': 'Option 7', 'number': 7, 'votes': 17, 'postproc': 0},
                {'option': 'Option 2', 'number': 2, 'votes': 12, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_mayoria_absoluta4(self):
        data = {
            'type': 'MAYORIA_ABSOLUTA',
            'options': [
                {'option': 'PP', 'number': 1, 'votes': 10867344},
                {'option': 'PSOE', 'number': 2, 'votes': 7003511},
                {'option': 'CiU', 'number': 3, 'votes': 1015691},
                {'option': 'IU', 'number': 4, 'votes': 1686040},
            ]
        }

        expected_result = [
                {'option': 'PP', 'number': 1, 'votes': 10867344, 'postproc': 1},
                {'option': 'PSOE', 'number': 2, 'votes': 7003511, 'postproc': 0},
                {'option': 'IU', 'number': 4, 'votes': 1686040, 'postproc': 0},
                {'option': 'CiU', 'number': 3, 'votes': 1015691, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
        
