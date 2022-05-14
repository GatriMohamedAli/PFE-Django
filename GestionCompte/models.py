from django.db import models

# Create your models here.
from general.models import Utilisateur


class Administrateur (Utilisateur):
    def __str__(self):
        return self.nom