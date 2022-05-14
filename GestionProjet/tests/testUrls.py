from django.test import SimpleTestCase
from django.urls import reverse, resolve
from GestionProjet.views import *

class TestUrls(SimpleTestCase):

    def test_home_responsable(self):
        url = reverse('acceuil')
        self.assertEquals(resolve(url).func, home)

    def test_listeChef(self):
        url = reverse('chefs')
        self.assertEquals(resolve(url).func, listeChef)

    def test_modifier_projet(self):
        url = reverse('modifier_projet', args="3")
        self.assertEquals(resolve(url).func, modifier_projet)

    def test_chefProjet(self):
        url = reverse('chef_projet')
        self.assertEquals(resolve(url).func, list_projet)

    def test_addarticle(self):
        url = reverse('ajouter_article', args=["2"])
        self.assertEquals(resolve(url).func, ajouter_article)

    def test_addarticle2(self):
        url = reverse('ajouter_article2', args=["2", "2"])
        self.assertEquals(resolve(url).func, ajouter_article2)

    def test_comfirmer_article(self):
        url = reverse('comfirmer_article', args=["2", "2"])
        self.assertEquals(resolve(url).func, comfirmer_article)

    def test_supprimer_projet(self):
        url = reverse('supprimer_projet', args="3")
        self.assertEquals(resolve(url).func, supprimer_projet)

    def test_ajout_projet(self):
        url = reverse('ajout_projet')
        self.assertEquals(resolve(url).func, ajouter_projet)

    def test_searchTache(self):
        url = reverse('searchTache')
        self.assertEquals(resolve(url).func, search_Tache)

    def test_liste_Projet(self):
        url = reverse('liste_Projet')
        self.assertEquals(resolve(url).func, listprojet)

    def test_acceuil_Chef(self):
        url = reverse('acceuil_Chef')
        self.assertEquals(resolve(url).func, homechef)   

    def test_detaille_projet(self):
        url = reverse('detaille_projet', args="1")
        self.assertEquals(resolve(url).func, detaille_projet)

    def test_ajout_tache(self):
        url = reverse('ajout_tache', args="1")
        self.assertEquals(resolve(url).func, ajout_tache)

    def test_terminer_projet(self):
        url = reverse('terminer_projet', args="1")
        self.assertEquals(resolve(url).func, terminer_projet)

    def test_modifier_tache(self):
        url = reverse('modifier_tache', args=["1","1"])
        self.assertEquals(resolve(url).func, modifier_tache) 

    def test_supprimer_tache(self):
        url = reverse('supprimer_tache', args=["1","1"])
        self.assertEquals(resolve(url).func, supprimer_tache)   

    def test_statproj(self):
        url = reverse('statproj')
        self.assertEquals(resolve(url).func, statProj)   
         
    def test_pdf(self):
        url = reverse('pdf', args="1")
        self.assertEquals(resolve(url).func,GeneratePdf.as_view())                       