from django.db import models

# Create your models here.
class Utilisateur (models.Model):
    ROLE = (
                ('admin', 'admin'),
                ('Responsable', 'Responsable'),
                ('chefProjet', 'chefProjet'),
                ('ResponsableMagasin','ResponsableMagasin')
            )
    image = models.FileField(upload_to='static/images', null=True, blank=True)
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    age = models.IntegerField()
    date_naiss = models.DateField()
    adresse = models.CharField(max_length=800, null=True)
    email = models.CharField(max_length=800, null=True)
    telephone = models.CharField(max_length=8, null=True)
    role = models.CharField(max_length=200, null=True, choices=ROLE)
    motDePasse = models.CharField(max_length=50)

    def __str__(self):
        return self.nom