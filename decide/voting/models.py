from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from base import mods
from base.models import Auth, Key

#Votaciones binarias

#Modelo votación binaria
class VotacionBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()

    def str(self):
        return self.titulo
        
    #Contea el número de Si (true) emitido en la votación binaria
    def Numero_Trues(self):
        return RespuestaBinaria.objects.filter(respuesta=1,votacionBinaria_id=self.id).count()

    #Contea el número de No (false) emitido en la votación binaria
    def Numero_Falses(self):
        return RespuestaBinaria.objects.filter(respuesta=0,votacionBinaria_id=self.id).count()

    #Añade una respuesta binaria a la votación del mismo tipo 
    #Cuando creemos la respuesta binaria solo le tendremos que indicar los atributos de la respuesta en sí (el sentir del voto)
    #La función entonces asociará la respuesta binaria emitida a la pregunta binaria en cuestión  
    def addRespuestaBinaria(self,respuestaBinaria):
        respuestaBinaria.votacionBinaria = self
        respuestaBinaria.save()


#Modelo respuesta binaria
class RespuestaBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    votacionBinaria = models.ForeignKey(VotacionBinaria,on_delete = models.CASCADE)
    respuesta = models.BooleanField(choices =[(1,('Sí')),(0,('No'))])

    def Nombre_Votacion(self):
        return self.votacionBinaria.titulo


#Votaciones Preferencia
class VotacionPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    def __str__(self):
        return self.titulo
    
    
    #Devuelve el número de preguntas que tiene asociada una votación preferencia
    def Numero_De_Preguntas_Preferencia(self):
        return PreguntaPreferencia.objects.filter(votacionPreferencia_id=self.id).count()

    
    #Añade una pregunta preferencia a la votación preferencia
    #Al crear la pregunta preferencia solo es necesario indicar el atributo textopregunta
    #La función asocia directamente la pregunta preferencia a la votación preferencia que se le ha indicado
    def addPreguntaPreferencia(self, preguntaPreferencia):
        preguntaPreferencia.votacionPreferencia = self
        preguntaPreferencia.save()


class PreguntaPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    votacionPreferencia = models.ForeignKey(VotacionPreferencia,on_delete = models.CASCADE)
    textoPregunta = models.CharField(max_length=50)
    def Nombre_Votacion_Preferencia(self):
        return self.votacionPreferencia.titulo
    def __str__(self):
        return self.textoPregunta

    #Devuelve el número de opciones existentes en la pregunta
    def Numero_De_Opciones(self):
        return OpcionRespuesta.objects.filter(preguntaPreferencia_id=self.id).count()

    #Añade una respuesta a la pregunta preferencia
    #Al crear la respuesta solo es necesario el atributo nombre_opcion
    #La función asocia directamente la respuesta con la pregunta preferencia indicada
    def addOpcionRespuesta(self, opcionRespuesta):
        opcionRespuesta.preguntaPreferencia = self
        opcionRespuesta.save()


class OpcionRespuesta(models.Model):
    id = models.AutoField(primary_key=True)
    preguntaPreferencia = models.ForeignKey(PreguntaPreferencia,on_delete = models.CASCADE)
    nombre_opcion = models.CharField(max_length=100)
    def Nombre_Pregunta_Preferencia(self):
        return self.preguntaPreferencia.textoPregunta
    def __str__(self):
        return self.nombre_opcion
    
    #Añade una respuesta preferencia a la respuesta
    #Al crear la respuesta preferencia solo es necesario el atributo orden_preferencia
    #La función asocia directamente la respuesta preferencia con la respuesta indicada
    def addRespuetaPreferencia(self, respuestaPreferencia):
        respuestaPreferencia.opcionRespuesta = self
        respuestaPreferencia.save()


    #Devuelve la media de preferencia de la opción en función de las respuestas dadas a esa opción
    def Media_Preferencia(self):
        respuestas = RespuestaPreferencia.objects.filter(opcionRespuesta=self.id).values('orden_preferencia')
        n_respuestas = len(respuestas)
        if n_respuestas == 0:  ##Evita la división por cero
            n_respuestas = 1
        total = 0
        for value in respuestas:
            total = total + value['orden_preferencia']
        return total / n_respuestas

    
    #Para cada opción devuelve un diccionario con el siguiente formato:
    #(POS1: X veces), (POS2: Y veces), ... ,(POSN: Z veces)
    #Donde POS es la posición de preferencia donde se ha colocado dicha opción y 'X', 'Y' y 'Z' son el nº de veces que se ha indicado en esa posición
    def Respuestas_Opcion(self):
        respuestas = RespuestaPreferencia.objects.filter(opcionRespuesta=self.id).values('orden_preferencia')
        result = {}

        for value in respuestas:
            if value['orden_preferencia'] in result:
                result[value['orden_preferencia']] = result[value['orden_preferencia']] + 1
            else:
                result[value['orden_preferencia']] = 1

        for key in result:
            result[key] = str(result[key]) + " veces"

        print(result)
        return sorted(result.items())


class RespuestaPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    opcionRespuesta = models.ForeignKey(OpcionRespuesta,on_delete = models.CASCADE)
    orden_preferencia = models.PositiveIntegerField(blank=True, null=True)
    def Nombre_Opcion_Respuesta(self):
        return self.opcionRespuesta.nombre_opcion


#Votación
class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(default=1)

    VOTING_TYPE_OPTIONS = [
        ('IDENTITY', 'IDENTITY'),
        ('WEBSTER', 'WEBSTER'),
        ('DHONT', 'DHONT'),
        ('RECUENTO_BORDA', 'RECUENTO_BORDA'),
        ('RELATIVA', 'RELATIVA'),
        ('MAYORIA_ABSOLUTA', 'MAYORIA_ABSOLUTA'),
        ('HAMILTON', 'HAMILTON'),
        ('SUBTRAC', 'SUBTRAC')]

    voting_type= models.CharField(max_length=50,choices=VOTING_TYPE_OPTIONS,default='IDENTITY')
    
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]
    
    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
