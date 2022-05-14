# Generated by Django 3.1.7 on 2021-06-20 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_article', models.CharField(max_length=100, null=True)),
                ('nom_article', models.CharField(max_length=100, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='magasin/images')),
                ('desc_article', models.TextField()),
                ('dispo_article', models.IntegerField()),
                ('categorie', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=100)),
                ('listarticles', models.TextField()),
                ('telephone', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('commentaire', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsable_Magasin',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general.utilisateur')),
            ],
            bases=('general.utilisateur',),
        ),
        migrations.CreateModel(
            name='Constituer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=0)),
                ('date_ajout', models.DateTimeField(auto_now_add=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Magasin.article')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Magasin.commande')),
            ],
            options={
                'unique_together': {('commande', 'article')},
            },
        ),
    ]
