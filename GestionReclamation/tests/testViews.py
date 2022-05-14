from django.test import TestCase, Client
from django.urls import reverse
from urllib import urlencode
import _datetime
from datetime import date
from general.models import *
from GestionReclamation import *


class Testviews(TestCase):
    def setUp(self):

        utilisateur = Utilisateur()
        utilisateur.nom = "ABC"
        utilisateur.prenom = "ABC"
        utilisateur.age = 22
        utilisateur.date_naiss = date(1998, 9, 16)
        utilisateur.adresse = "RADES Meliane"
        utilisateur.email = "medalygatry@live.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "Responsable"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()

        utilisateur = Utilisateur()
        utilisateur.nom = "ABC"
        utilisateur.prenom = "ABC"
        utilisateur.age = 22
        utilisateur.date_naiss = date(1998, 9, 16)
        utilisateur.adresse = "RADES Meliane"
        utilisateur.email = "medalygatry@live.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "chefProjet"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()


        rec=Reclamation()
        rec.service="Projet"
        rec.objet="Problem"
        rec.description_reclamation="PROBLEM"
        rec.date_creation=_datetime.date.today()
        rec.statut="en attente"
        rec.utilisateur=Utilisateur.objects.get(pk="2")
        rec.save()

        rec2=Reclamation()
        rec2.service="Projet22"
        rec2.objet="Problem22"
        rec2.description_reclamation="PROBLEM22"
        rec2.date_creation=_datetime.date.today()
        rec2.statut="en attente"
        rec2.utilisateur=Utilisateur.objects.get(pk="2")
        rec2.save()

        solu=Solution()
        solu.num_solution=0
        solu.description_solution="do this"
        solu.date_solution=_datetime.date.today()
        solu.reclamation=Reclamation.objects.get(pk="1")
        solu.utilisateur=Utilisateur.objects.get(pk="2")
        solu.save()


        self.listRec=reverse('listReclamation')
        self.ajoutRec=reverse('ajouterReclamation')
        self.modRec=reverse('modifierReclamation', args="3")
        self.suppRec=reverse('supprimerReclamation', args="3")
        self.traitRec=reverse('TraitementReclamation', args="2")
        self.termRec=reverse('TreminerReclamation', args="2")
        self.listSolu=reverse('listSolutionReclamation')
        self.ajoutSolu=reverse('ajouterSolution', args="1")
        self.detSolu=reverse('detaille', args=["1","1"])
        self.modSolu=reverse('modifierSolution', args=["1","1"] )
        self.suppSolu=reverse('supprimerSolution', args=["1","2"]  )


    def test_listRec_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.listRec)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/list_reclamation.html')   

    def test_ajoutRec_view(self):
        self.client.session['id']="2"
        data=urlencode({
            'service': 'IT',
            'objet': 'recl2',
            'description_reclamation': 'recl2',
            'date_creation': '2021/06/10',
            'statut': 'en attente' ,
            'utilisateur': '2'
            
        })
        response=self.client.POST(self.ajoutRec, data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/ajouter_reclamation.html')   


    def test_modRec_view(self):
        self.client.session['id']="2"
        data=urlencode({
            'service': 'IT',
            'objet': 'recl2EDITED',
            'description_reclamation': 'recl2EDITED',
            'date_creation': '2021/06/10',
            'statut': 'en attente' ,
            'utilisateur': '2'
            
        })
        response=self.client.POST(self.modRec,data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/modifier_reclamation.html')   


    def test_suppRec_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.suppRec)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/supprimer_reclamation.html')   

    def test_traitRec_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.traitRec)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/list_reclamation.html')   


    def test_termRec_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.termRec)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/list_reclamation.html')   


    def test_listSolu_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.listSolu)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/list_solution.html')   


    def test_ajoutSolu_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'num_solution': '22',
            'description_solution': 'soluu',
            'date_solution': '2021/06/12',
            'reclamation': '1',
            'utilisateur': '1' 
            
            
        })
        response=self.client.POST(self.ajoutSolu,data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/ajouter_solution_reclamation.html')   



    def test_detSolu_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.detSolu)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/detaille.html')   


    def test_modSolu_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'num_solution': '22',
            'description_solution': 'solu EDITED',
            'date_solution': '2021/06/12',
            'reclamation': '1',
            'utilisateur': '1' 
            
            
        })
        response=self.client.POST(self.modSoludata, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/modifier_solution.html')   


    def test_suppSolu_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.suppSolu)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/supprimer_solution.html')   

