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


#Tests Ley D'Hont
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
        
        
  #Tests de SUSTRACCION
    def test_substrat_1(self):
        seats = 8
        data = {
            'seats': seats,
            'type': 'SUBTRAC',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes_add': 10, 'votes_subtract':12},
                {'option': 'Option 2', 'number': 2, 'votes_add': 5, 'votes_subtract':2},
                {'option': 'Option 3', 'number': 3, 'votes_add': 6, 'votes_subtract':1},
                {'option': 'Option 4', 'number': 4, 'votes_add': 8, 'votes_subtract':2},
                {'option': 'Option 5', 'number': 5, 'votes_add': 2, 'votes_subtract':0},

            ]
        }

        expected_result = [
            {'option': 'Option 4', 'number': 4, 'votes_add': 8, 'votes_subtract':2, 'votes': 6, 'postproc': 3},
            {'option': 'Option 3', 'number': 3, 'votes_add': 6, 'votes_subtract':1, 'votes': 5, 'postproc': 3},
            {'option': 'Option 2', 'number': 2, 'votes_add': 5, 'votes_subtract':2, 'votes': 3, 'postproc': 1},
            {'option': 'Option 5', 'number': 5, 'votes_add': 2, 'votes_subtract':0, 'votes': 2, 'postproc': 1},
            {'option': 'Option 1', 'number': 1, 'votes_add': 10, 'votes_subtract':12, 'votes': 0, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_substrat_2(self):
        seats = 300
        data = {
            'seats': seats,
            'type': 'SUBTRAC',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes_add': 10032, 'votes_subtract':2345},
                {'option': 'Option 2', 'number': 2, 'votes_add': 423, 'votes_subtract':22},
                {'option': 'Option 3', 'number': 3, 'votes_add': 8002, 'votes_subtract':4231},
                {'option': 'Option 4', 'number': 4, 'votes_add': 1235, 'votes_subtract':1932},
                {'option': 'Option 5', 'number': 5, 'votes_add': 9012, 'votes_subtract':230},
                {'option': 'Option 6', 'number': 6, 'votes_add': 7000, 'votes_subtract': 4000},

            ]
        }

        expected_result = [
            {'option': 'Option 5', 'number': 5, 'votes_add': 9012, 'votes_subtract': 230, 'votes': 8782, 'postproc': 111},
            {'option': 'Option 1', 'number': 1, 'votes_add': 10032, 'votes_subtract': 2345, 'votes': 7687,'postproc': 98},
            {'option': 'Option 3', 'number': 3, 'votes_add': 8002, 'votes_subtract': 4231, 'votes': 3771,'postproc':48},
            {'option': 'Option 6', 'number': 6, 'votes_add': 7000, 'votes_subtract': 4000, 'votes': 3000,'postproc': 38},
            {'option': 'Option 2', 'number': 2, 'votes_add': 423, 'votes_subtract': 22, 'votes': 401, 'postproc': 5},
            {'option': 'Option 4', 'number': 4, 'votes_add': 1235, 'votes_subtract':1932, 'votes': 0, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_substrat_no_options(self):
        seats = 300
        data = {
            'seats': seats,
            'type': 'SUBTRAC',

        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_substrat_no_type(self):
        seats = 300
        data = {
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes_add': 10032, 'votes_subtract':2345},
                {'option': 'Option 2', 'number': 2, 'votes_add': 423, 'votes_subtract':22},
                {'option': 'Option 3', 'number': 3, 'votes_add': 8002, 'votes_subtract':4231},
                {'option': 'Option 4', 'number': 4, 'votes_add': 1235, 'votes_subtract':1932},
                {'option': 'Option 5', 'number': 5, 'votes_add': 9012, 'votes_subtract':230},
                {'option': 'Option 6', 'number': 6, 'votes_add': 7000, 'votes_subtract': 4000},

            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_substrat_no_seats(self):
        data = {
            'type': 'SUBTRAC',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes_add': 10, 'votes_subtract':12},
                {'option': 'Option 2', 'number': 2, 'votes_add': 5, 'votes_subtract':2},
                {'option': 'Option 3', 'number': 3, 'votes_add': 6, 'votes_subtract':1},
                {'option': 'Option 4', 'number': 4, 'votes_add': 8, 'votes_subtract':2},
                {'option': 'Option 5', 'number': 5, 'votes_add': 2, 'votes_subtract':0},

            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)      
        

    def test_hamilton_1(self):
        seats = 10
        data = {
            'type': 'HAMILTON',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 15},
                {'option': 'Option 2', 'number': 2, 'votes': 3},
                {'option': 'Option 3', 'number': 3, 'votes': 12},
                {'option': 'Option 4', 'number': 4, 'votes': 0}
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 15, 'postproc': 5},
            {'option': 'Option 3', 'number': 3, 'votes': 12, 'postproc': 4},
            {'option': 'Option 2', 'number': 2, 'votes': 3, 'postproc': 1},
            {'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_hamilton_2(self):
        seats = 9
        data = {
            'type': 'HAMILTON',
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 10},
                {'option': 'Option 2', 'number': 2, 'votes': 6},
                {'option': 'Option 3', 'number': 3, 'votes': 10},
                {'option': 'Option 4', 'number': 4, 'votes': 5},
                {'option': 'Option 5', 'number': 5, 'votes': 0}
            ]
        }

        expected_result = [
                {'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 3},
                {'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 3},
                {'option': 'Option 2', 'number': 2, 'votes': 6, 'postproc': 2},
                {'option': 'Option 4', 'number': 4, 'votes': 5, 'postproc': 1},
                {'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    # Test donde no se le pasa las variables options
    def test_no_options_hamilton(self):
        seats = 5
        data = {
            'type': 'HAMILTON',
            'seats': seats
        }
        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_no_seats_hamilton(self):
        data = {
            'type': 'HAMILTON',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 15},
                {'option': 'Option 2', 'number': 2, 'votes': 12},
                {'option': 'Option 3', 'number': 3, 'votes': 3},
                {'option': 'Option 4', 'number': 4, 'votes': 0}

            ]
        }
        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_no_type_hamilton(self):
        seats = 12
        data = {
            'seats': seats,
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 15},
                {'option': 'Option 2', 'number': 2, 'votes': 12},
                {'option': 'Option 3', 'number': 3, 'votes': 3},
                {'option': 'Option 4', 'number': 4, 'votes': 0}
            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_webster1(self):
        data = {
            'type': 'WEBSTER',
            'seats': 10,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 7 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 4 },
            { 'option': 'Option 3', 'number': 3, 'votes': 7, 'postproc': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 1 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_webster2(self):
        data = {
            'type': 'WEBSTER',
            'seats': 12,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 4', 'number': 4, 'votes': 3 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 9 },
                { 'option': 'Option 7', 'number': 7, 'votes': 0 },
                { 'option': 'Option 8', 'number': 8, 'votes': 0 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 3 },
            { 'option': 'Option 6', 'number': 6, 'votes': 9, 'postproc': 3 },
            { 'option': 'Option 3', 'number': 3, 'votes': 8, 'postproc': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 4', 'number': 4, 'votes': 3, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 7', 'number': 7, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 8', 'number': 8, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Test de algoritmo de webster con bastantes más datos y asientos
    def test_webster3(self):
        data = {
            'type': 'WEBSTER',
            'seats': 30,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 31 },
                { 'option': 'Option 2', 'number': 2, 'votes': 19 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 4', 'number': 4, 'votes': 3 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 9 },
                { 'option': 'Option 7', 'number': 7, 'votes': 4 },
                { 'option': 'Option 8', 'number': 8, 'votes': 0 },
                { 'option': 'Option 9', 'number': 1, 'votes': 15 },
                { 'option': 'Option 10', 'number': 2, 'votes': 6 },
                { 'option': 'Option 11', 'number': 3, 'votes': 9 },
                { 'option': 'Option 12', 'number': 4, 'votes': 19 },
                { 'option': 'Option 13', 'number': 5, 'votes': 16 },
                { 'option': 'Option 14', 'number': 6, 'votes': 6 },
                { 'option': 'Option 15', 'number': 7, 'votes': 0 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 31, 'postproc': 6 } ,
            { 'option': 'Option 2', 'number': 2, 'votes': 19, 'postproc': 4 },
            { 'option': 'Option 12', 'number': 4, 'votes': 19, 'postproc': 4 },
            { 'option': 'Option 13', 'number': 5, 'votes': 16, 'postproc': 3 },
            { 'option': 'Option 9', 'number': 1, 'votes': 15, 'postproc': 3 },
            { 'option': 'Option 6', 'number': 6, 'votes': 9, 'postproc': 2 },
            { 'option': 'Option 11', 'number': 3, 'votes': 9, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 10', 'number': 2, 'votes': 6, 'postproc': 1 },
            { 'option': 'Option 14', 'number': 6, 'votes': 6, 'postproc': 1 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 1 },
            { 'option': 'Option 7', 'number': 7, 'votes': 4, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 3, 'postproc': 1 },
            { 'option': 'Option 8', 'number': 8, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 15', 'number': 7, 'votes': 0, 'postproc': 0 }
                           ]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        print(values)
        self.assertEqual(values, expected_result)

    # Test donde no se le pasa las variables options
    def test_no_options_webster(self):
        seats = 5
        data = {
            'type': 'WEBSTER',
            'seats': seats
        }
        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_no_seats_webster(self):
        data = {
            'type': 'WEBSTER',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 31 },
                { 'option': 'Option 2', 'number': 2, 'votes': 19 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 14', 'number': 6, 'votes': 6 },
                { 'option': 'Option 15', 'number': 7, 'votes': 0 },
            ]
        }
        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_no_type_webster(self):
        seats = 12
        data = {
            'seats': seats,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 31 },
                { 'option': 'Option 2', 'number': 2, 'votes': 19 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 14', 'number': 6, 'votes': 6 },
                { 'option': 'Option 15', 'number': 7, 'votes': 0 },
            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 400)

        values = response.json()
        self.assertEqual(values, expected_result)