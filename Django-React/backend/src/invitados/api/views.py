from rest_framework.generics import ListAPIView
from invitados.models import Invitado
from .serializers import InvitadoSerializer

class InvitadoListView(ListAPIView):
    queryset = Invitado.objects.all()
    serializer_class = InvitadoSerializer


class InvitadoDetailView(ListAPIView):
    queryset = Invitado.objects.all()
    serializer_class = InvitadoSerializer
