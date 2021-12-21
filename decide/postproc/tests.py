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


    def test_dhont_1(self):
        seats = 9
        data = {
            'type': 'DHONT',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100},
                {'option': 'Option 2', 'number': 2, 'votes': 122},
                {'option': 'Option 3', 'number': 3, 'votes': 500},
                {'option': 'Option 4', 'number': 4, 'votes': 279},
                {'option': 'Option 5', 'number': 5, 'votes': 927},
            ]
        }

        expected_result = [

            {'option': 'Option 5', 'number': 5, 'votes': 927, 'postproc': 5},
            {'option': 'Option 3', 'number': 3, 'votes': 500, 'postproc': 3},
            {'option': 'Option 4', 'number': 4, 'votes': 279, 'postproc': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 122, 'postproc': 0},
            {'option': 'Option 1', 'number': 1, 'votes': 100, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)


        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhont_2(self):
        seats = 5
        data = {
            'type': 'DHONT',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 10},
                {'option': 'Option 2', 'number': 2, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votes': 6},
                {'option': 'Option 4', 'number': 4, 'votes': 4},
                {'option': 'Option 5', 'number': 5, 'votes': 10},
                {'option': 'Option 6', 'number': 6, 'votes': 2},
                {'option': 'Option 7', 'number': 7, 'votes': 6},
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 2},
            {'option': 'Option 5', 'number': 5, 'votes': 10, 'postproc': 1},
            {'option': 'Option 3', 'number': 3, 'votes': 6, 'postproc': 1},
            {'option': 'Option 7', 'number': 7, 'votes': 6, 'postproc': 1},
            {'option': 'Option 4', 'number': 4, 'votes': 4, 'postproc': 0},
            {'option': 'Option 6', 'number': 6, 'votes': 2, 'postproc': 0},
            {'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_dhont_3(self):
        seats = 8
        data = {
            'type': 'DHONT',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 340},
                {'option': 'Option 2', 'number': 2, 'votes': 280},
                {'option': 'Option 3', 'number': 3, 'votes': 110},
                {'option': 'Option 4', 'number': 4, 'votes': 150},
                {'option': 'Option 5', 'number': 5, 'votes': 160},
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 340, 'postproc': 3},
            {'option': 'Option 2', 'number': 2, 'votes': 280, 'postproc': 2},
            {'option': 'Option 5', 'number': 5, 'votes': 160, 'postproc': 1},
            {'option': 'Option 4', 'number': 4, 'votes': 150, 'postproc': 1},
            {'option': 'Option 3', 'number': 3, 'votes': 110, 'postproc': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        self.assertEqual(values, expected_result)        

    def test_dhont_4(self):
        seats = 90
        data = {
            'type': 'DHONT',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 7600},
                {'option': 'Option 2', 'number': 2, 'votes': 8300},
                {'option': 'Option 3', 'number': 3, 'votes': 5150},
                {'option': 'Option 4', 'number': 4, 'votes': 4400},
                {'option': 'Option 5', 'number': 5, 'votes': 7700},
            ]
        }

        expected_result = [

            {'option': 'Option 2', 'number': 2, 'votes': 8300, 'postproc': 22},
            {'option': 'Option 5', 'number': 5, 'votes': 7700, 'postproc': 21},
            {'option': 'Option 1', 'number': 1, 'votes': 7600, 'postproc': 21},
            {'option': 'Option 3', 'number': 3, 'votes': 5150, 'postproc': 14},
            {'option': 'Option 4', 'number': 4, 'votes': 4400, 'postproc': 12},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
       
    def test_recuento_borda1(self):
        data = {
            'type': 'RECUENTO_BORDA',
            'order_options': [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 80},
                {'option': 'Option 2', 'number': 2, 'order_number': '1', 'votes': 15},
                {'option': 'Option 3', 'number': 3, 'order_number': '1', 'votes': 5},
                {'option': 'Option 1', 'number': 1, 'order_number': '2', 'votes': 5},
                {'option': 'Option 2', 'number': 2, 'order_number': '2', 'votes': 80},
                {'option': 'Option 3', 'number': 3, 'order_number': '2', 'votes': 15},
                {'option': 'Option 1', 'number': 1, 'order_number': '3', 'votes': 15},
                {'option': 'Option 2', 'number': 2, 'order_number': '3', 'votes': 5},
                {'option': 'Option 3', 'number': 3, 'order_number': '3', 'votes': 80},
            ]
        }

        expected_result = [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 80, 'postproc': 265},
                {'option': 'Option 2', 'number': 2, 'order_number': '1', 'votes': 15, 'postproc': 210},
                {'option': 'Option 3', 'number': 3, 'order_number': '1', 'votes': 5, 'postproc': 125},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        print(values)
        self.assertEqual(values, expected_result)

    def test_recuento_borda2(self):
        data = {
            'type': 'RECUENTO_BORDA',
            'order_options': [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 50},
                {'option': 'Option 2', 'number': 2, 'order_number': '1', 'votes': 50},
                {'option': 'Option 3', 'number': 3, 'order_number': '1', 'votes': 0},
                {'option': 'Option 1', 'number': 1, 'order_number': '2', 'votes': 20},
                {'option': 'Option 2', 'number': 2, 'order_number': '2', 'votes': 20},
                {'option': 'Option 3', 'number': 3, 'order_number': '2', 'votes': 60},
                {'option': 'Option 1', 'number': 1, 'order_number': '3', 'votes': 30},
                {'option': 'Option 2', 'number': 2, 'order_number': '3', 'votes': 30},
                {'option': 'Option 3', 'number': 3, 'order_number': '3', 'votes': 40},
            ]
        }

        expected_result = [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 50, 'postproc': 220},
                {'option': 'Option 2', 'number': 2, 'order_number': '1', 'votes': 50, 'postproc': 220},
                {'option': 'Option 3', 'number': 3, 'order_number': '1', 'votes': 0, 'postproc': 160},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    #Test en el que se le pasa una votación normal, no una con order_options
    def test_recuento_borda_no_order_options(self):
        data = {
            'type': 'RECUENTO_BORDA',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 10},
                {'option': 'Option 2', 'number': 2, 'votes': 5},
                {'option': 'Option 3', 'number': 3, 'votes': 6},
                {'option': 'Option 4', 'number': 4, 'votes': 8},
                {'option': 'Option 5', 'number': 5, 'votes': 4},
                {'option': 'Option 6', 'number': 6, 'votes': 6},
                {'option': 'Option 7', 'number': 7, 'votes': 2},
                {'option': 'Option 8', 'number': 8, 'votes': 0},

            ],
            'order_options': []
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Test en el que no se le pasa tipo a una votación de borda
    def test_borda_no_type(self):

        data = {
            'order_options': [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 50},
                {'option': 'Option 2', 'number': 2, 'order_number': '1', 'votes': 50},
                {'option': 'Option 3', 'number': 3, 'order_number': '1', 'votes': 0},
                {'option': 'Option 1', 'number': 1, 'order_number': '2', 'votes': 20},
                {'option': 'Option 2', 'number': 2, 'order_number': '2', 'votes': 20},
                {'option': 'Option 3', 'number': 3, 'order_number': '2', 'votes': 60},
                {'option': 'Option 1', 'number': 1, 'order_number': '3', 'votes': 30},
                {'option': 'Option 2', 'number': 2, 'order_number': '3', 'votes': 30},
                {'option': 'Option 3', 'number': 3, 'order_number': '3', 'votes': 40},
            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Test en el que todos los votos son 0, así viene de votación al no haber ningún
    #equipo de cabina que pueda realizar votaciones
    def test_borda_cero_votos(self):
        data = {
            'type': 'RECUENTO_BORDA',
            'order_options': [
                {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'order_number': '2', 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'order_number': '3', 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'order_number': '4', 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'order_number': '5', 'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'order_number': '1', 'votes': 0, 'postproc': 0},
            {'option': 'Option 2', 'number': 2, 'order_number': '2', 'votes': 0, 'postproc': 0},
            {'option': 'Option 3', 'number': 3, 'order_number': '3', 'votes': 0, 'postproc': 0},
            {'option': 'Option 4', 'number': 4, 'order_number': '4', 'votes': 0, 'postproc': 0},
            {'option': 'Option 5', 'number': 5, 'order_number': '5', 'votes': 0, 'postproc': 0}]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        print(values)
        self.assertEqual(values, expected_result)
        
