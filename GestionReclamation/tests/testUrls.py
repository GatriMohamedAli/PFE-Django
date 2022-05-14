from django.test import SimpleTestCase
from django.urls import reverse, resolve
from GestionReclamation import *


class TestUrls(SimpleTestCase):

    def test_search(self):
        url=reverse('search')
        self.assertEquals(resolve(url).func, search_results)

    def test_search_solution(self):
        url=reverse('search_solution')
        self.assertEquals(resolve(url).func, search_results_solution)

    def test_TreminerReclamation(self):
        url=reverse('TreminerReclamation', args="1")
        self.assertEquals(resolve(url).func, TreminerReclamation)

    def test_TraitementReclamation(self):
        url=reverse('TraitementReclamation', args="1")
        self.assertEquals(resolve(url).func, TraitementReclamation)

    def test_listReclamation(self):
        url=reverse('listReclamation')
        self.assertEquals(resolve(url).func, listReclamation)


    def test_ajouterReclamation(self):
        url=reverse('ajouterReclamation')
        self.assertEquals(resolve(url).func, ajouterReclamation)


    def test_supprimerReclamation(self):
        url=reverse('supprimerReclamation', args="1")
        self.assertEquals(resolve(url).func, search_supprimerReclamationresults)

    def test_modifierReclamation(self):
        url=reverse('modifierReclamation', args="1")
        self.assertEquals(resolve(url).func, modifierReclamation)

    def test_listSolutionReclamation(self):
        url=reverse('listSolutionReclamation', args="1")
        self.assertEquals(resolve(url).func, listSolutionReclamation)

    def test_ajouterSolution(self):
        url=reverse('ajouterSolution', args="1")
        self.assertEquals(resolve(url).func, ajouterSolutionReclamation)


    def test_detaille(self):
        url=reverse('detaille', args=["1","2"])
        self.assertEquals(resolve(url).func, detaille)

    def test_supprimerSolution(self):
        url=reverse('supprimerSolution', args=["1","2"])
        self.assertEquals(resolve(url).func, supprimerSolution)

    def test_modifierSolution(self):
        url=reverse('modifierSolution', args=["1","2"])
        self.assertEquals(resolve(url).func, modifierSolution)