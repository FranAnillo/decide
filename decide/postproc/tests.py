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


    def test_relativa1(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 7 },
                { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                { 'option': 'Option 3', 'number': 3, 'votes': 6 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 7, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 6, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_relativa2(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2 },
                { 'option': 'Option 2', 'number': 2, 'votes': 8 },
            ]
        }

        expected_result = [
            { 'option': 'Option 2', 'number': 2, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 1', 'number': 1, 'votes': 2, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_relativa3(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 4 },
            ]
        }

        expected_result = [
            { 'option': 'Option 4', 'number': 4, 'votes': 4, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 0 },
            { 'option': 'Option 1', 'number': 1, 'votes': 1, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_relativa4(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
            ]
        }

        expected_result = [
                { 'option': 'Option 3', 'number': 3, 'votes': 8, 'postproc': 1 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 0 },
                { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_relativa5(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 0 },
                { 'option': 'Option 8', 'number': 8, 'votes': 0 },
                { 'option': 'Option 9', 'number': 9, 'votes': 1 },
                { 'option': 'Option 10', 'number': 10, 'votes': 0 },
                { 'option': 'Option 11', 'number': 11, 'votes': 0 },
                { 'option': 'Option 12', 'number': 12, 'votes': 0 },
                { 'option': 'Option 13', 'number': 13, 'votes': 0 },
                { 'option': 'Option 14', 'number': 14, 'votes': 0 },
                { 'option': 'Option 15', 'number': 15, 'votes': 0 },
            ]
        }

        expected_result = [
                { 'option': 'Option 9', 'number':9, 'votes': 1, 'postproc': 1 },
                { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 8', 'number': 8, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 10', 'number': 10, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 11', 'number': 11, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 12', 'number': 12, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 13', 'number': 13, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 14', 'number': 14, 'votes': 0, 'postproc': 0 },
                { 'option': 'Option 15', 'number': 15, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_relativa6(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 70 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 345 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200 },
                { 'option': 'Option 5', 'number': 5, 'votes': 729 },
                { 'option': 'Option 6', 'number': 6, 'votes': 273},
            ]
        }

        expected_result = [
                { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 1 },
                { 'option': 'Option 5', 'number': 5, 'votes': 729, 'postproc': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 345, 'postproc': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 273, 'postproc': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200, 'postproc': 0 },
                { 'option': 'Option 1', 'number': 1, 'votes': 70, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_relativa7(self):
        data = {
            'type': 'RELATIVA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 7230 },
                { 'option': 'Option 2', 'number': 2, 'votes': 82300 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3445 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20320 },
                { 'option': 'Option 5', 'number': 5, 'votes': 72952 },
                { 'option': 'Option 6', 'number': 6, 'votes': 27213},
                { 'option': 'Option 7', 'number': 7, 'votes': 83200 },
                { 'option': 'Option 8', 'number': 8, 'votes': 34455 },
                { 'option': 'Option 9', 'number': 9, 'votes': 20321 },
                { 'option': 'Option 10', 'number': 10, 'votes': 729123 },
                { 'option': 'Option 11', 'number': 11, 'votes': 27243},
                { 'option': 'Option 12', 'number': 12, 'votes': 802120 },
                { 'option': 'Option 13', 'number': 13, 'votes': 343235 },
                { 'option': 'Option 14', 'number': 14, 'votes': 20230 },
                { 'option': 'Option 15', 'number': 15, 'votes': 721239 },
                { 'option': 'Option 16', 'number': 16, 'votes': 273123},
            ]
        }

        expected_result = [
                { 'option': 'Option 12', 'number': 12, 'votes': 802120, 'postproc': 1 },
                { 'option': 'Option 10', 'number': 10, 'votes': 729123, 'postproc': 0 },
                { 'option': 'Option 15', 'number': 15, 'votes': 721239, 'postproc': 0 },
                { 'option': 'Option 13', 'number': 13, 'votes': 343235, 'postproc': 0 },
                { 'option': 'Option 16', 'number': 16, 'votes': 273123, 'postproc': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 83200, 'postproc': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 82300, 'postproc': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 72952, 'postproc': 0 },
                { 'option': 'Option 8', 'number': 8, 'votes': 34455, 'postproc': 0 },
                { 'option': 'Option 11', 'number': 11, 'votes': 27243, 'postproc': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 27213, 'postproc': 0 },
                { 'option': 'Option 9', 'number': 9, 'votes': 20321, 'postproc': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20320, 'postproc': 0 },
                { 'option': 'Option 14', 'number': 14, 'votes': 20230, 'postproc': 0 },
                { 'option': 'Option 1', 'number': 1, 'votes': 7230, 'postproc': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3445, 'postproc': 0 },
              
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)
