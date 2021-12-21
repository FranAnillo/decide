from rest_framework.views import APIView
from rest_framework.response import Response


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



def post(self, request):
        """
         * type: IDENTITY | DHONT | RELATIVA | ABSOLUTA | BORDA | SUBTRAC
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
        p = request.data.get('paridad')

        if len(opts) == 0 and len(order_opts) == 0:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'RELATIVA':
            return self.relativa(opts)
        elif t == 'ABSOLUTA':
            return self.absoluta(opts)
        elif t == 'BORDA':
            if len(order_opts) == 0:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return self.borda(order_opts)
        elif t == 'SUBTRAC':
            if (s == None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.subtrac(opts, s))
