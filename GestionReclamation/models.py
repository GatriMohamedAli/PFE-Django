
from django.db.models import Q

from GestionProjet import models
from django.db import models

# Create your models here.
from general.models import Utilisateur


class Reclamation(models.Model):
    STATUT = (('en attente', 'en attente'),
            ('prise en charge', 'prise en charge'),
            ('en traitement', 'en traitement'),
            ('terminé', 'terminé'))
    ABOUT = (('Projet', 'Projet'),
             ('Magasin', 'Magasin'),
             ('IT', 'IT'),
             ('RH', 'RH'))
    service = models.CharField(max_length=200, null=False,choices=ABOUT, default='Choose me')
    objet = models.CharField(max_length=200, null=False)
    description_reclamation = models.TextField(null=False, blank=False)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    statut = models.CharField(max_length=200, null=False, choices=STATUT)
    utilisateur = models.ForeignKey(Utilisateur, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.objet



class Solution(models.Model):
    num_solution = models.IntegerField(null=False)
    description_solution = models.TextField(null=False)
    date_solution = models.DateField(auto_now_add=True,null=False)
    reclamation = models.ForeignKey(Reclamation, null=True, on_delete=models.SET_NULL)
    utilisateur = models.ForeignKey(Utilisateur, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.num_solution