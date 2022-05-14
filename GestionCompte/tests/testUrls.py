from django.test import SimpleTestCase
from django.urls import reverse, resolve
from GestionCompte.views import *


class TestUrls(SimpleTestCase):

    def test_home_admin(self):
        url = reverse('Administrateur')
        self.assertEquals(resolve(url).func, home)

    def test_statProj(self):
        url = reverse('StatProj')
        self.assertEquals(resolve(url).func, listeChef)

    def test_StatMag(self):
        url = reverse('StatMag')
        self.assertEquals(resolve(url).func, modifier_projet)

    def test_StatRec(self):
        url = reverse('StatRec')
        self.assertEquals(resolve(url).func, list_projet)

    def test_liste_Utilisateur(self):
        url = reverse('liste_Utilisateur', args='Responsable')
        self.assertEquals(resolve(url).func, ajouter_article)

    def test_ajouter_utilisateur(self):
        url = reverse('ajouter_utilisateur')
        self.assertEquals(resolve(url).func, ajouter_article2)

    def test_supprimer_utilisateur(self):
        url = reverse('supprimer_utilisateur')
        self.assertEquals(resolve(url).func, comfirmer_article)

    def test_modifier_utilisateur(self):
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

        url = reverse('modifier_utilisateur', args="1")
        self.assertEquals(resolve(url).func, supprimer_projet)

    def test_profile_utilisateur(self):
        url = reverse('profile_utilisateur')
        self.assertEquals(resolve(url).func, ajouter_projet)

    def test_modifier_profile(self):
        url = reverse('modifier_profile')
        self.assertEquals(resolve(url).func, ajouter_projet)

    def test_modifier_passe(self):
        url = reverse('modifier_passe')
        self.assertEquals(resolve(url).func, ajouter_projet)                
