# Generated by Django 3.1.7 on 2021-06-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magasin', '0002_remove_constituer_date_ajout'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituer',
            name='codeUnique',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
