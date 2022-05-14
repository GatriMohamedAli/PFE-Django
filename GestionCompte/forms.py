

from django import forms
from django.forms import NumberInput

from GestionProjet.models import Responsable_Projet, Chef_Projet
from Magasin.models import Responsable_Magasin
from general.models import Utilisateur
from django.db import models
def validate_letters(word):
    for char in word:
        if not char.isalpha() and char != " ":
            return False
    return True
class UtilisateurForm(forms.ModelForm):
    date_naiss = forms.DateField(widget=NumberInput(
        attrs={'type': 'date'}), error_messages={'required': "Ce champ est obligatoire"})
    motDePasse = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': (
        'Password'), 'class': 'form-control'}), error_messages={'required': "Ce champ est obligatoire"})
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control',
            'placeholder': ('seuemail@email.com'),
            'required': 'required'
        }),
        error_messages={'invalid': 'veuillez respecter le format email :seuemail@email.com ', 'required': "Ce champ est obligatoire"})

    class Meta:
        model = Utilisateur
        fields = '__all__'
        widgets = {
        }
        error_messages = {

            'nom': {'required': "Ce champ est obligatoire", },
            'prenom': {'required': "Ce champ est obligatoire", },
            'age': {'required': "Ce champ est obligatoire", },
            'date_naiss': {'required': "Ce champ est obligatoire", },
            'chef_projet': {'required': "Ce champ est obligatoire", },
            'adresse': {'required': "Ce champ est obligatoire", },
            'telephone': {'required': "Ce champ est obligatoire", },
            'role': {'required': "Ce champ est obligatoire", },
            'motDePasse': {'required': "Ce champ est obligatoire", },
            'email': {'required': "Ce champ est obligatoire", },
        }

    def clean_nom(self):
        cleaned_data = super().clean()
        data = forms.nom = cleaned_data.get('nom')
        if not data.islower():
            raise forms.ValidationError("Obligatoire,le nom devrait être en minuscule")
        if not validate_letters(data):
            raise forms.ValidationError("le nom ne doit pas contenir de caractères spéciaux.")
            data.strip()
        return data

    def clean_prenom(self):
        cleaned_data = super().clean()
        data= forms.prenom = cleaned_data.get('prenom')
        if not data.islower():
            raise forms.ValidationError("Obligatoire,le prénom projet devrait être en minuscule")
        if not validate_letters(data):
            raise forms.ValidationError("le nom ne doit pas contenir de caractères spéciaux.")
            data.strip()
        return data

    def clean_adresse(self):
        data = self.cleaned_data['adresse']
        if not data.islower():
            raise forms.ValidationError("L'adresse devrait être en minuscule")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError("L'adresse ne doit pas commancer de caractères spéciaux.")
        return data

    def clean_age(self):
        cleaned_data = super().clean()
        forms.age = cleaned_data.get('age')
        if forms.age <= 19:
            raise forms.ValidationError(
                "L'âge doit être positif et supérieur a 19!!")
        return forms.age

    def clean_telephone(self):
        cleaned_data = super().clean()
        forms.telephone = cleaned_data.get('telephone')
        if len(forms.telephone) < 8:
            raise forms.ValidationError(
                " Le numéro de téléphone doit être composé de 8 chiffres!!")
        if not forms.telephone.isdigit():
            raise forms.ValidationError(
                " Le numéro de téléphone doit être composé uniquement des chiffres !!")
        return forms.telephone


class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Responsable_Projet
        fields = '__all__'

    def clean(self):
        return self.cleaned_data


class ChefForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={'required': "Ce champ est obligatoire"})

    class Meta:
        model = Chef_Projet
        fields = '__all__'

        def clean(self):
            return self.cleaned_data


class ResponsableMagasinForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={'required': "Ce champ est obligatoire"})

    class Meta:
        model = Responsable_Magasin
        fields = '__all__'

        def clean(self):
            return self.cleaned_data


class confirm(forms.Form):
    motDePasse = models.CharField(max_length=50)
    new_password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

class FormConfirm(forms.Form):
    motDePasse = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('mot de passe acctuelle'), 'class': 'form-control'}), error_messages={'required': "Ce champ est obligatoire"})
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('nouveau mot de passe'), 'class': 'form-control'}), error_messages={'required': "Ce champ est obligatoire"})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Confirmez le mot de passe'), 'class': 'form-control'}), error_messages={'required': "Ce champ est obligatoire"})
    class Meta:
        model = confirm
        fields = '__all__'

    def clean_new_password(self):
        cleaned_data = super().clean()
        data = forms.new_password = cleaned_data.get('new_password')
        if len(data) < 5:
            raise forms.ValidationError("Obligatoire, Les mots de passe comportent au moins 5 caractères")
        return data
    def clean_confirm_password(self):
        cleaned_data = super().clean()
        data = forms.confirm_password = cleaned_data.get('confirm_password')
        new_password = cleaned_data.get('new_password')

        if len(data) < 5:
            raise forms.ValidationError("Obligatoire, Les mots de passe comportent au moins 5 caractères")
        if data != new_password:
            raise forms.ValidationError("Les mots de passe que vous avez entrés ne sont pas identiques.")
        return data