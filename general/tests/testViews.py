from django.test import TestCase, Client
from django.urls import reverse
from urllib import urlencode
from general.models import *



class Testviews(TestCase):
    def setUp(self):
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


        self.client=Client()
        self.login=reverse('')
        self.logout=reverse('logout')
        self.subscribe=reverse('subscribe')
        self.valider=reverse('valider', args=["medalygatry@live.com","547864"])
        self.success=reverse('success', args="medalygatry@live.com")

    def test_login_view(self):
       

        response=self.client.POST(self.login,{
            'email': 'medalygatry@live.com',
            'motDePasse' : 'ABC'
        })
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')    

    def test_logout_view():
        response=self.client.get(self.logout)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_success_view():
        response=self.client.POST(self.success,{
            'new_password' : 'DALI',
            'confirm_password' : 'DALI'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscribe/success.html.html')   


    def test_subscribe_view():
        data = urlencode({"Email": "medalygatry@live.com"})
        response=self.client.POST(self.subscribe, data, content_type="application/x-www-form-urlencoded")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'subscribe/index.html')   

    def test_valider_view():
        response=self.client.POST(self.valider,{
            'code':"547864"
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'subscribe/valider.html')               