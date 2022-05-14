from django.test import SimpleTestCase
from django.urls import reverse, resolve
from general.views import *
from general.models import *


class TestUrls(SimpleTestCase):

    def test_login(self):
        url=reverse('')
        self.assertEquals(resolve(url).func,login)

    def test_logout(self):
        url=reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_subscribe(self):
        url=reverse('subscribe')
        self.assertEquals(resolve(url).func, subscribe)

    def test_valider(self):
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


        url=reverse('valider', args=[utilisateur.email,"32157"])
        self.assertEquals(resolve(url).func, valider)            

    def test_success(self):
        utilisateur = Utilisateur()
        utilisateur.nom = "ABC"
        utilisateur.prenom = "ABC"
        utilisateur.age = 25
        utilisateur.date_naiss = date(1998, 9, 16)
        utilisateur.adresse = "RADES Meliane"
        utilisateur.email = "foulen@gmail.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "admin"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()

        url=reverse('success', args=[utilisateur.email])
        self.assertEquals(resolve(url).func, success)   