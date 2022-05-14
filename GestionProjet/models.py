from django.urls import reverse
from django.db import models
from django.db.models import Q
# Create your models here.
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from GestionProjet.custom_validators import validate_interval
from Magasin.models import Article
from general.models import Utilisateur


def __str__(self):
        return self.nom

class Responsable_Projet (Utilisateur):
    def __str__(self):
        return self.nom


class Chef_Projet (Utilisateur):
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reversed("", kwargs={"ch": self.id})


class Projet (models.Model):
    ETAT = (('a faire', 'a faire'),
            ('en cours', 'en cours'),
            ('terminé', 'terminé'))
    nom_projet = models.CharField(max_length=100, null=False)
    description_projet = models.TextField(blank=True)
    adresse_projet = models.CharField(max_length=200, null=False)
    date_ajout_projet = models.DateTimeField(auto_now_add=True)
    cout_projet = models.FloatField(null=True, validators=[validate_interval])
    delai_projet = models.PositiveIntegerField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    etat_projet = models.CharField(max_length=200, null=True, choices=ETAT)
    caracteristique_projet = models.TextField(blank=True)
    chef_projet = models.ForeignKey(Chef_Projet, null=True, on_delete=models.SET_NULL)

    # Create / Insert / Add - POST
    # Retrieve / Fetch - GET
    # Update / Edit - PUT
    # Delete / Remove - DELETE

    def __str__(self):
        return self.nom_projet
    def get_absolute_url(self):
        return reverse('app:detail',args=[self.id],)


class Tache(models.Model):
    titre_tache = models.CharField(max_length=200, null=False)
    description_tache = models.TextField(null=False, blank=False)
    mots_clés = models.CharField(max_length=1000,null=False)
    demarche_tache = models.TextField(null=True, blank=True)
    difficulté_tache = models.TextField(null=True, blank=True)
    projet = models.ForeignKey(Projet, null=True, on_delete=models.SET_NULL)


class DetailleAffectation(models.Model):
    projet = models.ForeignKey(Projet, null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=False, on_delete=models.CASCADE)
    chef_projet = models.ForeignKey(
    Chef_Projet, null=True, on_delete=models.SET_NULL)
    nombre = models.IntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True, null=True)
