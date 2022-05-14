from django.forms import ModelForm
from django import forms

from Magasin.models import Article, Commande


class ArticleAdd(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class CommandeAdd(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'
        widgets = {
        }
        error_messages = {
            'adresse': {'required': "Ce champ est obligatoire",},
        }
