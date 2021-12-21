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

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | DHONT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type')
        opts = request.data.get('options', [])
        order_opts = request.data.get('order_options', [])
        s = request.data.get('seats')
        p = request.data.get('paridad')

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'DHONT':
            if(s==None):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if (p==True):
                   results = self.dhont(opts, s)
                   return Response(self.aplicarParidad(results))
                else:    
                    return Response(self.dhont(opts, s))

        return Response({})
