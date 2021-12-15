from django.contrib import admin
from django.utils import timezone

from .models import *

from .filters import StartedFilter

#Votaciones Binarias
class RespuestaBinariaInline(admin.TabularInline):
    model = RespuestaBinaria
    extra = 1

#Creadión de la visualización de votaciones binarias para un admin
class VotacionBinariaAdmin(admin.ModelAdmin):
    list_display=('id','titulo','descripcion','Numero_Trues','Numero_Falses')
    inlines =[RespuestaBinariaInline] 

#Creadión de la respuesta de votaciones binarias para un admin
class RepuestaBinariaAdmin(admin.ModelAdmin):
    list_display = ('id','respuesta','Nombre_Votacion')

#Votaciones preferencias
class PreguntaPreferenciaInline(admin.TabularInline):
    model = PreguntaPreferencia
    extra = 1

class VotacionPreferenciaAdmin(admin.ModelAdmin):
    list_display=('id','titulo','descripcion','Numero_De_Preguntas_Preferencia')
    inlines =[PreguntaPreferenciaInline]

class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 1

class PreguntaPreferenciaAdmin(admin.ModelAdmin):
    list_display = ('id','textoPregunta','Nombre_Votacion_Preferencia','Numero_De_Opciones')
    inlines =[OpcionRespuestaInline]

class RespuestaPreferenciaInline(admin.TabularInline):
    model = RespuestaPreferencia
    extra = 1

class OpcionRespuestaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_opcion','Nombre_Pregunta_Preferencia','Media_Preferencia','Respuestas_Opcion')
    inlines =[RespuestaPreferenciaInline]

class RespuestaPreferenciaAdmin(admin.ModelAdmin):
    list_display = ('id','orden_preferencia','Nombre_Opcion_Respuesta')


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(VotacionBinaria,VotacionBinariaAdmin)
admin.site.register(RespuestaBinaria,RepuestaBinariaAdmin)

admin.site.register(VotacionPreferencia,VotacionPreferenciaAdmin)
admin.site.register(PreguntaPreferencia, PreguntaPreferenciaAdmin)
admin.site.register(OpcionRespuesta,OpcionRespuestaAdmin)
admin.site.register(RespuestaPreferencia,RespuestaPreferenciaAdmin)
