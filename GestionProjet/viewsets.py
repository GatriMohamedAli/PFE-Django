from rest_framework import viewsets
from . import models
from . import serializers

class ProjetViewset(viewsets.ModelViewSet):
    queryset = models.Projet.objects.all()
    serializer_class = serializers.ProjetSerializer