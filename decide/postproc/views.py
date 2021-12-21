from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
        elif t == 'DHONT':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if (p==True):
                   results = self.dhont(opts, s)
                   return Response(self.aplicarParidad(results))
                else:    
                    return Response(self.dhont(opts, s))
        elif t == 'WEBSTER':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.webster(opts, s))
        elif t=='WEBSTERMOD':
            if(s==None):
                return Response([], status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.webster_mod(opts, s))
        elif t == 'HAMILTON':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(self.hamilton(opts, s))            
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})
        