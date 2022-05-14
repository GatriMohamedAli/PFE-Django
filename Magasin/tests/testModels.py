from django.test import TestCase
from Magasin.models import *


class TestModels(TestCase):

    def test_ArticleModel(self):
        article = Article()
        article.code_article = "RJ541"
        article.cat_article = "Cable"
        article.nom_article = "Cable"
        article.desc_article = "Cable"
        article.dispo_article = 20
        article.save()

        record = Article.objects.get(pk=1)
        self.assertEquals(record, article)


    def test_CommandeModel(self):
        cmd = Commande()
        cmd.mail = "medalygatry@gmail.com"
        cmd.listarticles = "RJ54-15"
        cmd.telephone = "26789456"
        cmd.adresse = "Rades Meliane"
        cmd.status = "Pending"
        cmd.commentaire = "URGENT"
        cmd.save()

        record = Commande.objects.get(pk=1)
        self.assertEquals(record, cmd)