from django.test import TestCase
from general.models import *
from datetime import date


class TestModels(TestCase):

    def test_Utilisateur(self):
        utilisateur = Utilisateur()
        utilisateur.nom = "ABC"
        utilisateur.prenom = "ABC"
        utilisateur.age = 25
        utilisateur.date_naiss = date(1998, 9, 16)
        utilisateur.adresse = "RADES Meliane"
        utilisateur.email = "medalygatry@live.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "admin"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()
        record = Utilisateur.objects.get(pk=1)
        self.assertEquals(record, Utilisateur)