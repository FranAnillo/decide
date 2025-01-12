from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import copy

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)



    def mayoria_absoluta(self, options):
        out= []
        numvotos=0

        for opt in options:
            numvotos=opt['votes']+numvotos
            out.append({
                **opt,
                'postproc':0,
            })
        if len(out)>=2:
            cocientes = []
            for i in range(len(out)):
                cocientes.append(out[i]['votes']/numvotos)
            ganador=cocientes.index(max(cocientes))
            mayor=cocientes[ganador]

            if mayor>0.5:
                out[ganador]['postproc']= 1
        else:
            out[0]['postproc']= 1
                
        out.sort(key=lambda x:-x['votes'])
        return Response(out)
        
   
    def recuento_borda(self, order_options):
        #Creación de la salida y de una lista auxiliar para filtrar la entrada
        #y que en la salida solo aparezca una ocurrencia por opción
        out = []
        aux = []
        for ord in order_options:
            if ord['option'] not in aux:
                out.append({
                    **ord,
                    'postproc': 0,
                })
            aux.append(ord['option'])
        if len(order_options) == 0:
            out.sort(key=lambda x: -x['postproc'])
            return Response(out)
        else:
            #Número de opciones distintas que hay (no de entradas)
            numOptions = max(out,key=lambda x: x['number'])['number']

            #Creación de una lista que guarda de 1 a numOptions de manera inversa
            #para después usarlo para calcular la puntuación
            puntos = [0]
            j = numOptions
            while j>=1:
                puntos.append(j)
                j-=1

            #Lista que servirá para ir almacenando la suma de los votos de las distintas opciones
            votos = []
            i=0
            while i<=numOptions:
                votos.append(0)
                i+=1

            #Recorrer los datos de entrada, obteniendo la opción y los votos de dicha opción
            #en la posición seleccionada, para después multiplicarlo y obtener la puntuación real
            for ord in order_options:
                opcion = int(ord['number'])
                mult = puntos[int(ord['order_number'])]
                votos[opcion] = votos[opcion] + mult*int(ord['votes'])

            #Asignar a la salida, en el parámetro postproc, la puntuación total de cada opción
            cont=0
            while cont<numOptions:
                out[cont]['postproc'] = votos[cont+1]
                cont+=1

            out.sort(key=lambda x: -x['postproc'])
            return Response(out)
            
    def dhont(self, options, seats):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': 0,
            });

        escaños = 0
        while escaños < seats:
            cocientes = []
            for i in range(len(out)):
                cocientes.append(out[i]['votes'] / (out[i]['postproc'] + 1))

            ganador = cocientes.index(max(cocientes))
            out[ganador]['postproc'] = out[ganador]['postproc'] + 1
            escaños += 1

        out.sort(key=lambda x: -x['votes'])
        return out
      
      
    #Metodo de votacion de algoritmo relativo
    def relativa(self, options):
        out= []
        numvotos=0

        for opt in options:
            numvotos=opt['votes']+numvotos
            out.append({
                **opt,
                'postproc':0,
            })

        mayor=0.0
        list=out.copy()
        while len(list)>=2:

            if len(list)>2:
                cocientes = []
                for i in range(len(list)):
                   cocientes.append(list[i]['votes']/numvotos)       
                perdedor=cocientes.index(min(cocientes))
                ganador=cocientes.index(max(cocientes))
                mayor=cocientes[ganador]
                if mayor>0.5:
                    g=list[ganador]['number']
                    out[g-1]['postproc']= 1
                    break
                numvotos= numvotos - cocientes[perdedor]
                del list[perdedor]
            elif len(list)==2:
                cocientes = []
                for i in range(len(list)):
                    cocientes.append(list[i]['votes']/numvotos)
                ganador=cocientes.index(max(cocientes)) 
                g=list[ganador]['number'] 
                out[g-1]['postproc']= 1
                break
        out.sort(key=lambda x:-x['votes'])
        return Response(out)


    def subtrac(self, options, seats):
        out = []

        for opt in options:

            votes = opt['votes_add'] - opt['votes_subtract']
            if votes < 0:
                votes = 0

            out.append({
                **opt,
                'votes':votes,
                'postproc': 0,
            })

        return self.dhont(out, seats)

    def hamilton(self, options, seats):
        out = []
        numvotos=0

        for opt in options:
            numvotos=opt['votes']+numvotos
            out.append({
                **opt,
                'postproc': 0,
            })

        
        for i in range(len(out)):
            cuota=((out[i]['votes']/numvotos)*seats)
            out[i]['postproc'] = out[i]['postproc'] + round(cuota)

        out.sort(key=lambda x: -x['votes'])
        return out
   
    def webster(self, options, seats):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': 0,
            })

        asientos = 0
        while asientos < seats:
            cocientes = []
            for i in range(len(out)):
                cocientes.append(out[i]['votes'] / (2 * out[i]['postproc'] + 1))

            ganador = cocientes.index(max(cocientes))
            out[ganador]['postproc'] = out[ganador]['postproc'] + 1
            asientos += 1

        out.sort(key=lambda x: -x['votes'])
        return out

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | RELATIVA | DHONT | MAYORIA_ABSOLUTA | RECUENTO_BORDA | SUBTRAC | HAMILTON
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
	    * seats: int
        """
        t = request.data.get('type')
        opts = request.data.get('options', [])
        order_opts = request.data.get('order_options', [])
        s = request.data.get('seats')

        
        if len(opts) == 0 and len(order_opts) == 0:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        elif t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'RELATIVA':
            return self.relativa(opts)
        elif t == 'MAYORIA_ABSOLUTA':
            return self.mayoria_absoluta(opts)
        elif t == 'RECUENTO_BORDA':
            if len(order_opts) == 0:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return self.recuento_borda(order_opts)
        elif t == 'SUBTRAC':
            if (s == None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.subtrac(opts, s))
        elif t == 'DHONT':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                results = self.dhont(opts, s)
                return Response(results)
        elif t == 'HAMILTON':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.hamilton(opts, s))
        elif t == 'WEBSTER':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.webster(opts, s))           
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})
