import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt

from mixnet.models import Auth
from voting.models import *

#Test de guardado de una votación binaria y comprobar que lo ha hecho correctamente
class GuardaVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb = VotacionBinaria(titulo="Titulo 1",descripcion="Descripcion")
        vb.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb=None
    def testExist(self):
        vb = VotacionBinaria.objects.get(titulo="Titulo 1")
        self.assertEquals(vb.titulo,"Titulo 1")
        self.assertEquals(vb.descripcion,"Descripcion")

#Crea una votación nueva, posteriormente la actualiza y comprueba que la actualización ha sido realizada con éxito
class ActualizaVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb = VotacionBinaria(titulo="Titulo 1",descripcion="Descripcion")
        vb.save()
        vb.titulo = "Titulo 2"
        vb.descripcion = "Description"
        vb.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb=None
    def testActualizado(self):
        vb = VotacionBinaria.objects.get(titulo="Titulo 2")
        self.assertEquals(vb.titulo,"Titulo 2")
        self.assertEquals(vb.descripcion,"Description")

#Crea una votación binaria, después crea una segunda, posteriormente la elimina y comprueba que se ha eliminado correctamente la segunda votación
class BorraVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="Titulo 1",descripcion="Descripcion 1")
        vb1.save()
        vb2 = VotacionBinaria(titulo="Titulo 2",descripcion="Descripcion 2")
        vb2.save()
        vb2.delete()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.vb2=None
    def testBorrado(self):
        totalVotaciones = len(VotacionBinaria.objects.all())
        self.assertEquals(totalVotaciones,1)

#Creación de una respuesta binaria a partir de una votación binaria
class AddRespuestaBinaria(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="Titulo 1",descripcion="Descripcion 1")
        vb1.save()
        rb1  = RespuestaBinaria(respuesta = 1)
        vb1.addRespuestaBinaria(rb1)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.rb1=None
    def testAdd(self):
        vb = VotacionBinaria.objects.get(titulo="Titulo 1")
        rb = RespuestaBinaria.objects.get(votacionBinaria_id=vb.id)
        self.assertEquals(rb.respuesta,1)
        self.assertEquals(rb.votacionBinaria_id,vb.id)

#Creación de una votación binaria con 4 respuestas para el conteo de true y false
class CuentaTruesYFalsesTest(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="Titulo 1",descripcion="Descripcion 1")
        vb1.save()

        rb1 = RespuestaBinaria(respuesta=1)
        rb2 = RespuestaBinaria(respuesta=1)
        rb3 = RespuestaBinaria(respuesta=1)
        rb4 = RespuestaBinaria(respuesta=0)

        vb1.addRespuestaBinaria(rb1)
        vb1.addRespuestaBinaria(rb2)
        vb1.addRespuestaBinaria(rb3)
        vb1.addRespuestaBinaria(rb4)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.rb1=None
        self.rb2=None
        self.rb3=None
        self.rb4=None
    def testContador(self):
        vb = VotacionBinaria.objects.get(titulo="Titulo 1")
        self.assertEquals(vb.Numero_De_Trues(),3)
        self.assertEquals(vb.Numero_De_Falses(),1)

class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')
