from django.test import TestCase, Client
from django.urls import reverse
from urllib import urlencode
import _datetime
from datetime import date
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
        utilisateur.role = "ResponsableMagasin"
        utilisateur.motDePasse = "ABC"
        utilisateur.save()


        self.client=Client()
        self.client.session['id']="1"

        self.home=reverse('article_list')
        self.commander=reverse('commander')
        self.modComm=reverse('editcomm', args="1")
        self.ajoutArt=reverse('article_create')
        self.ModArt=reverse('article_update', args="1")
        self.suppArt=reverse('article_delete', args="1")
        self.stat=reverse('stat')


    def test_home_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/article_list.html')

    def test_commander_view(self):
        self.client.session['id']="1"
        response=self.client.POST(self.commander,{
            'liste[]': 'RJ54-20',
            'adresse': 'rades meliane',
            'commentaire': 'URGENT'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/commander.html')


    def test_modComm_view(self):
        self.client.session['id']="1"
        response=self.client.POST(self.modComm{
            'liste[]': 'RJ54-20',
            'adresse': 'rades meliane EDITED',
            'commentaire': 'URGENT'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/editcomm.html')


    def test_ajoutArt_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'code_article': 'RJ44',
            'nom_article':  'Cable',
            'desc_article': 'write something',
            'dispo_article': 20,
            'categorie': 'Cable'
        })
        response=self.client.POST(self.ajoutArt,data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/ajouter_article.html')


    def test_ModArt_view(self):
        self.client.session['id']="1"
        data=urlencode({
            'code_article': 'RJ44',
            'nom_article':  'Cable EDITED',
            'desc_article': 'write somethingEDITED',
            'dispo_article': 20,
            'categorie': 'Cable'
        })
        response=self.client.POST(self.ModArt,data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/modifier_article.html')


    def test_suppArt_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.suppArt)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/supprimer_article.html')


    def test_stat_view(self):
        self.client.session['id']="1"
        response=self.client.get(self.stat)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'magasin/Responsable/stat.html')

