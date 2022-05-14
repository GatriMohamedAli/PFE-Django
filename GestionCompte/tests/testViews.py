from django.test import TestCase, Client
from django.urls import reverse
from urllib import urlencode
from general.models import *



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
        utilisateur.role = "admin"
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


        self.client=Client()
        self.client.session["id"]="1"

        self.home=reverse('Administrateur')
        self.statproj=reverse('statProj')
        self.statmag=reverse('statMag')
        self.statrec=reverse('statRec')
        self.listeusersResp=reverse('liste_Utilisateur', args="Responsable")
        self.listeusersChef=reverse('liste_Utilisateur', args="chefProjet")
        self.listeusersMag=reverse('liste_Utilisateur', args="ResponsableMagasin")
        self.ajoutuser=reverse('ajouter_utilisateur')
        self.moduser=reverse('supprimer_utilisateur', args="2")
        self.suppuser=reverse('modifier_utilisateur', args="2")
        self.prof=reverse('profile_utilisateur')
        self.modprof=reverse('modifier_profile')
        self.modpass=reverse('modifier_passe')

        def test_home_view(self):
            response=self.client.get(self.home)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/Administrateur.html') 


        def test_statproj_view(self):
            response=self.client.get(self.statproj)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/statAdmin.html')


        def test_statmag_view(self):
            response=self.client.get(self.statmag)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/statAdminMagasin.html')


        def test_statrec_view(self):
            response=self.client.get(self.statrec)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/statAdminRec.html')


        def test_listuserResp_view(self):
            response=self.client.get(self.listeusersResp)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/liste_ResponsablesProjets.html')


        def test_listuserChef_view(self):
            response=self.client.get(self.listeusersChef)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/liste_ChefProjet.html')


        def test_listuserMag_view(self):
            response=self.client.get(self.listeusersMag)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/liste_ResponsableMagasin.html')    


        def test_ajoutuser_view(self):
            data=urlencode({
                'nom': 'Dali',
                'prenom':'Dali',
                'age': '22',
                'date_naiss':'1998/09/16',
                'adresse': 'rades meliane',
                'email': 'foulen@live.com',
                'telephone': '26654489',
                'role': 'chefProjet',
                'motDePasse': 'ABC'
            })
            response=self.client.POST(self.ajoutuser,data, content_type="application/x-www-form-urlencoded")
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/ajouter_utilisateur.html')



        def test_moduser_view(self):
            data=urlencode({
                'nom': 'mohamed',
                'prenom':'ali',
                'age': '22',
                'date_naiss':'1998/09/16',
                'adresse': 'rades meliane',
                'email': 'foulen@live.com',
                'telephone': '26654489',
                'role': 'chefProjet',
                'motDePasse': 'hmid01'
            })
            response=self.client.POST(self.moduser,data, content_type="application/x-www-form-urlencoded")
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/modifier_utilisateur.html')


        def test_suppuser_view(self):
            response=self.client.POST(self.suppuser)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/supprimer_utilisateur.html')


        def test_profile_view(self):
            response=self.client.get(self.prof)
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/profile_utilisateur.html')


        def test_modprof_view(self):
            data=urlencode({
                'nom': 'mohamed',
                'prenom':'ali',
                'age': '22',
                'date_naiss':'1998/09/16',
                'adresse': 'rades meliane',
                'email': 'medalygatry@live.com',
                'telephone': '26654489',
                'role': 'admin',
                'motDePasse': 'hmid01'
            })
            response=self.client.POST(self.modprof,data, content_type="application/x-www-form-urlencoded")
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/modifier_profile.html')


        def test_modpass_view(self):
            response=self.client.POST(self.modpass,{
                'motDePasse': 'ABC',
                'new_password':'ali',
                'confirm_passwordge': 'ali'
            })
            self.assertEquals(response.status_code,200)
            self.assertTemplateUsed(response, 'compte/modifier_passe.html')


