from django.test import TestCase, Client
from django.urls import reverse
from urllib import urlencode
import _datetime
from datetime import date
from general.models import *
from Magasin.models import *
from GestionProjet.models import *


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
        utilisateur.email = "medalygatry@gmail.com"
        utilisateur.telephone = "26789456"
        utilisateur.role = "chefProjet"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()


        projet=Projet()
        projet.nom_projet="Proj1"
        projet.description_projet="Proj1"
        projet.adresse_projet="Proj1"
        projet.date_ajout_projet= _datetime.date.today()
        projet.cout_projet=3352
        projet.delai_projet=32
        projet.date_debut= date(2021, 6, 16)
        projet.date_fin= date(2021, 10, 16)
        projet.etat_projet='a faire'
        projet.caracteristique_projet="Proj1"
        projet.chef_projet=Utilisateur.objects.get(pk="2")
        projet.save()

        projet=Projet()
        projet.nom_projet="Proj2"
        projet.description_projet="Proj2"
        projet.adresse_projet="Proj2"
        projet.date_ajout_projet= _datetime.date.today()
        projet.cout_projet=3352
        projet.delai_projet=32
        projet.date_debut= date(2021, 6, 16)
        projet.date_fin= date(2021, 10, 16)
        projet.etat_projet='en cours'
        projet.caracteristique_projet="Proj2"
        projet.chef_projet=Utilisateur.objects.get(pk="2")
        projet.save()



        art=Article()
        art.code_article="RJ45"
        art.nom_article="Cable"
        art.desc_article="something here"
        art.dispo_article=20
        art.categorie="Cable"
        art.save()

        self.homeRes=reverse('acceuil')
        self.listChef=reverse('chefs')
        self.stat=reverse('statproj')
        self.listProj=reverse('liste_Projet')
        self.ajoutProj=reverse('ajout_projet')
        self.modProj=reverse('modifier_projet', args="3")
        self.suppProj=reverse('supprimer_projet', args="3")
        self.homeChef=reverse('acceuil_Chef')
        self.detProj=reverse('detaille_projet', args="2")
        self.ajoutTache=reverse('ajout_tache', args="2")
        self.TerProj=reverse('terminer_projet', args=" 1")
        self.modTache=reverse('modifier_tache', args=["1","2"])
        self.suppTache=reverse('supprimer_tache', args=["1","2"])
        self.ajoutArt=reverse('ajouter_article', args="2")
        self.ajoutArt2=reverse('ajouter_article2', args=["1","2"])
        self.comArt=reverse('comfirmer_article', args=["1","2"])
        self.pdf=reverse('pdf', args="2")





        self.client=Client()

    def test_homeres_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.homeRes)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/acceuil.html')    


    def test_listChef_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.listChef)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/list_chef.html')

    def test_stat_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.stat)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/stat.html')

    def test_listProj_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.listProj)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/list_projet.html')


    def test_ajoutProj_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'nom_projet': 'dali',
            'description_projet': 'dali',
            'adresse_projet': 'rades',
            'date_ajout_projet': '2021/06/10',
            'cout_projet': 3152,
            'delai_projet': 31,
            'date_debut': '2021/06/12',
            'date_fin': '2012/09/21',
            'etat_projet': 'a faire',
            'caracteristique_projet': 'proj',
            'chef_projet': '2'
        })
        response=self.client.POST(self.ajoutProj,data,content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/ajouter_projet.html')



    def test_modProj_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'nom_projet': 'daliEDITED',
            'description_projet': 'daliEDITED',
            'adresse_projet': 'rades',
            'date_ajout_projet': '2021/06/10',
            'cout_projet': 3152,
            'delai_projet': 31,
            'date_debut': '2021/06/12',
            'date_fin': '2012/09/21',
            'etat_projet': 'a faire',
            'caracteristique_projet': 'proj',
            'chef_projet': '2'
        })
        response=self.client.POST(self.modProj,data,content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/modifier_projet.html')


    def test_suppProj_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.suppProj)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/responsable_projet/supprimer_projet.html')



    def test_homeChef_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.homeChef)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/acceuil.html')

    def test_detProj_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.detProj)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/detaille_projet.html')

    def test_ajoutTache_view(self):
        self.client.session['id']="2"
        data=urlencode({
            'titre_tache':'Ajout Lamp',
            'description_tache': 'Ajout Lamp',
            'mots_clés': 'Lamp',
            'demarche_tache': 'Ajout Lamp',
            'difficulté_tache': 'facile',
            'projet': '2'
        })
        response=self.client.POST(self.ajoutTache,data,content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/ajout_tache.html')


    def test_TerProj_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.TerProj)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/liste_projets.html')


    def test_modTache_view(self):
        self.client.session['id']="2"
        data=urlencode({
            'titre_tache':'Ajout LampEDITED',
            'description_tache': 'Ajout LampEDITED',
            'mots_clés': 'Lamp',
            'demarche_tache': 'Ajout LampEDITED',
            'difficulté_tache': 'facile',
            'projet': '2'
        })
        response=self.client.POST(self.modTache,data,content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/modifier_tache.html')

    def test_suppTache_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.suppTache)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/supprimer_tache.html')


    def test_ajoutArt_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.ajoutArt)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/ajouter_article.html')

    def test_ajoutArt2_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.ajoutArt2)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/ajouter_article2.html')


    def test_comArt_view(self):
        self.client.session['id']="2"
        response=self.client.POST(self.comArt,{
            'number':15
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/comfirmer_article.html')



    def test_pdf_view(self):
        self.client.session['id']="2"
        response=self.client.get(self.pdf)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projet/chef_projet/pdf_detail.html')

