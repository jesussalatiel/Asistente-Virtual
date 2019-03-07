from rest_framework import serializers
from invitados.models import Invitado

class InvitadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitado
        fields = ('title', 'content')
