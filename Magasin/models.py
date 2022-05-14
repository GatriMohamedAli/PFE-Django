from django.db import models

# Create your models here.

from general.models import Utilisateur


class Article (models.Model):
    code_article = models.CharField(max_length=100, null=True, blank=False)
    nom_article = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='magasin/images', null=True, blank=True)
    desc_article = models.TextField()
    dispo_article = models.IntegerField()
    categorie = models.CharField(max_length=100, null=True)


class Responsable_Magasin (Utilisateur):
    def __str__(self):
        return self.nom


class Commande (models.Model):
    mail = models.CharField(max_length=100, null=False, blank=False)
    date_ajout = models.DateTimeField(auto_now_add=True, null=True)
    telephone = models.CharField(max_length=100, null=False, blank=False)
    adresse = models.CharField(max_length=100, null=False, blank=False)
    status = models.CharField(max_length=100, null=False, blank=False)
    commentaire = models.CharField(max_length=100, null=True, blank=True)


class Constituer(models.Model):
    commande = models.ForeignKey(
        Commande, null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=False, on_delete=models.CASCADE)
    qte = models.IntegerField(default=0)
    codeUnique = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        unique_together = (("commande", "article"),)
