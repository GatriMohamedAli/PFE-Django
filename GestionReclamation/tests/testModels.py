from django.test import TestCase
from GestionReclamation.models import *
from general.models import *
from datetime import date
import _datetime


class TestModels(TestCase):

    def test_Reclamtion(self):

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


        recl = Reclamation()
        recl.service = "Magasin"
        recl.objet = "article introuvable"
        recl.description_reclamation = "je viens pas de trouver l'article RJ54"
        recl.date_creation = _datetime.date.today()
        recl.statut = "en attente"
        recl.utilisateur = Utilisateur.objects.get(pk=1)
        recl.save()
        record = Reclamation.objects.get(pk=1)
        self.assertEquals(record, recl)


    def test_Solution(self):
        utilisateur = Utilisateur()
        utilisateur.nom = "ABC"
        utilisateur.prenom = "ABC"
        utilisateur.age = 25
        utilisateur.date_naiss = date(1998, 9, 16)
        utilisateur.adresse = "RADES Meliane"
        utilisateur.email = "foulen@live.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "admin"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()


        recl = Reclamation()
        recl.service = "IT"
        recl.objet = "Problem pc"
        recl.description_reclamation = "Mon pc ne marche pas"
        recl.date_creation = _datetime.date.today()
        recl.statut = "en attente"
        recl.utilisateur = Utilisateur.objects.get(email="foulen@live.com")
        recl.save()

        solu=Solution()
        solu.num_solution=
        solu.description_solution=
        solu.date_solution=
        solu.reclamation=Reclamation.object.get(objet="Problem pc")
        solu.utilisateur.objects.get(email="medalygatry@live.com")
        solu.save()

        record = Solution.objects.get(pk=1)
        self.assertEquals(record, solu)
