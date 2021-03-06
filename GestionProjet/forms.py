from django.forms import ModelForm
from django import forms

from .models import Projet, Article, Tache
from django.forms.widgets import NumberInput


def is_past_due(date_debut, date_fin):
    return date_fin > date_debut


def validate_digits_letters(word):
    for char in word:
        if not char.isdigit() and not char.isalpha():
            return False
    return True


def validate_digits_letters_espace(word):
    for char in word:
        if not char.isdigit() and not char.isalpha() and char != " " and char != "'":
            return False
    return True


class ProjetForm(forms.ModelForm):
    date_debut = forms.DateField(widget=NumberInput(
        attrs={'type': 'date'}), error_messages={'required': "Ce champ est obligatoire"})
    date_fin = forms.DateField(widget=NumberInput(
        attrs={'type': 'date'}), error_messages={'required': "Ce champ est obligatoire"})

    class Meta:
        model = Projet
        fields = '__all__'
        widgets = {
        }
        error_messages = {
            'nom_projet': {'required': "Ce champ est obligatoire", },
            'description_projet': {'required': "Ce champ est obligatoire", },
            'adresse_projet': {'required': "Ce champ est obligatoire", },
            'etat_projet': {'required': "Ce champ est obligatoire", },
            'chef_projet': {'required': "Ce champ est obligatoire", },
            'cout_projet': {'required': "Ce champ est obligatoire", },
        }
        help_texts = {
            'nom_projet': 'Obligatoire. Veuillez utiliser uniquement des alphabets et des chiffres en minuscules.',
            'description_projet': 'Veuillez utiliser uniquement des alphabets et des chiffres en minuscules.',
            'delai_projet': 'Delai de projet est un nombre des mois,Veuillez utiliser uniquement des chiffres.',
            'cout_projet': 'Nombre En DT,Veuillez utiliser uniquement des chiffres .',

        }

    def clean_nom_projet(self):
        data = self.cleaned_data['nom_projet']
        if not data.islower():
            raise forms.ValidationError(
                "nom de projet devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "nom de projet ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "nom de projet ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_adresse_projet(self):
        data = self.cleaned_data['adresse_projet']
        if not data.islower():
            raise forms.ValidationError(
                "L'adresse de projet devrait ??tre en minuscule")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "L'adresse de projet ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_description_projet(self):
        data = self.cleaned_data['description_projet']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,Description projet devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "Description projet ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "Description de projet ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_date_fin(self):
        cleaned_data = super().clean()
        forms.date_debut = cleaned_data.get('date_debut')
        forms.date_fin = cleaned_data.get('date_fin')
        if forms.date_debut and forms.date_fin:
            if not is_past_due(forms.date_debut, forms.date_fin):
                raise forms.ValidationError(
                    'date fin est superieur a date debut !!')
        return forms.date_fin


class ItemForm(ModelForm):
    class Meta:
        model = Projet
        fields = ['chef_projet']


class etatForm(ModelForm):
    class Meta:
        model = Projet
        fields = ['etat_projet']


class ArticleAdd(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class tacheFrom(forms.ModelForm):
    class Meta:
        model = Tache
        fields = '__all__'
        error_messages = {
            'titre_tache': {'required': "Ce champ est obligatoire", },
            'description_tache': {'required': "Ce champ est obligatoire", },
            'mots_cl??s': {'required': "Ce champ est obligatoire", },
        }

    def clean_description_tache(self):
        data = self.cleaned_data['description_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,Description de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "Description de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "Description de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_titre_tache(self):
        data = self.cleaned_data['titre_tache']
        if not data.islower():
            raise forms.ValidationError(
                "titre de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "titre de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "titre de t??che ne doit pas commancer de caract??res sp??ciaux.")
        for instance in Tache.objects.all():
            if instance.titre_tache == data:
                raise forms.ValidationError(
                    'Il ya une t??che avec le meme titre : ' + str(
                        data) + ',tu peut voir si m??me T??che ?')

        return data

    def clean_difficult??_tache(self):
        data = self.cleaned_data['difficult??_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,difficult?? de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "difficult?? de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "difficult?? de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_demarche_tache(self):
        data = self.cleaned_data['demarche_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,demarche de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "demarche de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "demarche de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_mots_cl??s(self):
        data = self.cleaned_data['mots_cl??s']
        if not data.islower():
            raise forms.ValidationError("mots cl??s devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "mots cl??s ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "mots cl??s ne doit pas commancer de caract??res sp??ciaux.")
        return data


class tacheUpdateFrom(forms.ModelForm):
    class Meta:
        model = Tache
        fields = '__all__'
        error_messages = {
            'titre_tache': {'required': "Ce champ est obligatoire", },
            'description_tache': {'required': "Ce champ est obligatoire", },
            'mots_cl??s': {'required': "Ce champ est obligatoire", },
        }

    def clean_mots_cl??s(self):
        data = self.cleaned_data['mots_cl??s']
        if not data.islower():
            raise forms.ValidationError("mots cl??s devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "mots cl??s ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "mots cl??s ne doit pas commancer de caract??res sp??ciaux.")

        return data

    def clean_description_tache(self):
        data = self.cleaned_data['description_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,Description de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "Description de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "Description de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_titre_tache(self):
        data = self.cleaned_data['titre_tache']
        if not data.islower():
            raise forms.ValidationError(
                "titre de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "titre de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "titre de t??che ne doit pas commancer de caract??res sp??ciaux.")

        return data

    def clean_difficult??_tache(self):
        data = self.cleaned_data['difficult??_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,difficult?? de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "difficult?? de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "difficult?? de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data

    def clean_demarche_tache(self):
        data = self.cleaned_data['demarche_tache']
        if not data.islower():
            raise forms.ValidationError(
                "Obligatoire,demarche de t??che devrait ??tre en minuscule")
        if not validate_digits_letters_espace(data):
            raise forms.ValidationError(
                "demarche de t??che ne doit pas contenir de caract??res sp??ciaux.")
            data.strip()
        if data[0] in "'":
            raise forms.ValidationError(
                "demarche de t??che ne doit pas commancer de caract??res sp??ciaux.")
        return data
