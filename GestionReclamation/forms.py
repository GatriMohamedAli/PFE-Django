
from django.forms import ModelForm
from django import forms
from django.forms.widgets import NumberInput
from django.template.defaultfilters import length

from .models import Reclamation, Solution
def validate_digits_letters_espace(word):
    for char in word:
        if not char.isdigit() and not char.isalpha() and char != " " and char != "'":
            return False
    return True
def validate_digits_letters(word):
    for char in word:
        if not char.isdigit():
            return False
    return True

class ReclamationForm(forms.ModelForm):
    objet= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required': "Ce champ est obligatoire"})
    description_reclamation = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),error_messages={'required': "Ce champ est obligatoire"})
    class Meta:
        model = Reclamation
        fields = '__all__'
        error_messages = {
            'objet': {'required': "Ce champ est obligatoire", },
            'statut': {'required': "Ce champ est obligatoire", },
            'utilisateur': {'required': "Ce champ est obligatoire", },
        }
        help_texts = {
            'objet': 'Obligatoire. Veuillez utiliser uniquement des alphabets et des chiffres en minuscules.',
            'description_reclamation': 'Veuillez utiliser uniquement des alphabets et des chiffres en minuscules.',
        }
    def clean_objet(self):
        objet = self.cleaned_data.get('objet')
        if not objet.islower():
            raise forms.ValidationError("Objet de réclamation doit être en minuscule")
        if not validate_digits_letters_espace(objet) or objet[0] in "'":
            raise forms.ValidationError("Objet de réclamationne doit pas contenir des caractères spéciaux.")
            objet.strip()
        for instance in Reclamation.objects.all():
            if instance.objet == objet:
                if instance.statut != 'terminé':
                    raise forms.ValidationError(
                        'Il ya une reclamtion avec le meme objet: ' + objet + ' non terminé, Tu peut voir si la solution est fiable ?')
        return objet

    def clean_description_reclamation(self):
        data = self.cleaned_data.get('description_reclamation')
        if not data.islower():
            raise forms.ValidationError("La description de réclamation devrait être en minuscule")
        if not validate_digits_letters_espace(data[0]) or "'" in data[0]:
            raise forms.ValidationError("La description de réclamationne doit pas commancer des caractères spéciaux.")
            data.strip()
        return data


class ReclamationUpdate(forms.ModelForm):
    objet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            error_messages={'required': "Ce champ est obligatoire"})
    description_reclamation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                              error_messages={'required': "Ce champ est obligatoire"})

    class Meta:
        model = Reclamation
        fields = '__all__'
        error_messages = {
            'objet': {'required': "Ce champ est obligatoire", },
            'statut': {'required': "Ce champ est obligatoire", },
            'utilisateur': {'required': "Ce champ est obligatoire", },
        }

    def clean_objet(self):
            objet = self.cleaned_data.get('objet')
            if not objet.islower():
                raise forms.ValidationError("Objet de réclamation doit être en minuscule")
            if not validate_digits_letters_espace(objet) or objet[0] in "'":
                raise forms.ValidationError("Objet de réclamationne doit pas contenir des caractères spéciaux.")
                objet.strip()
            return objet

    def clean_description_reclamation(self):
            data = self.cleaned_data.get('description_reclamation')
            if not data.islower():
                raise forms.ValidationError("La description de réclamation devrait être en minuscule")
            if not validate_digits_letters_espace(data[0]) or "'" in data[0]:
                raise forms.ValidationError(
                    "La description de réclamationne doit pas commancer des caractères spéciaux.")
                data.strip()
            return data

class SolutionForm(forms.ModelForm):
    num_solution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                            error_messages={'required': "Ce champ est obligatoire"})
    description_solution = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                              error_messages={'required': "Ce champ est obligatoire"})
    class Meta:
        model = Solution
        fields = '__all__'
        error_messages = {
            'num_solution': {'required': "Ce champ est obligatoire", },
            'description_solution': {'required': "Ce champ est obligatoire", },
        }
    def clean_num_solution(self):
            data = self.cleaned_data.get('num_solution')
            if not data > 0:
                raise forms.ValidationError(
                        "Le Numéro de solution doit etre positive.")
            for instance in Solution.objects.all():
                if instance.num_solution == data:
                    raise forms.ValidationError(
                        'Il ya une solution avec le meme numéro: ' + str(data) + ',tu peut voir si la solution est fiable ?')
            return data
    def clean_description_solution(self):
            data = self.cleaned_data.get('description_solution')
            if not data.islower():
                raise forms.ValidationError("La description de réclamation devrait être en minuscule")
            if not validate_digits_letters_espace(data[0]) or "'" in data[0]:
                raise forms.ValidationError(
                    "La description de réclamationne doit pas commancer par des caractères spéciaux.")
                data.strip()
            return data



class SolutionUpdateForm(forms.ModelForm):
    num_solution = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                            error_messages={'required': "Ce champ est obligatoire"})
    description_solution = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                              error_messages={'required': "Ce champ est obligatoire"})
    class Meta:
        model = Solution
        fields = '__all__'
        error_messages = {
            'num_solution': {'required': "Ce champ est obligatoire", },
            'description_solution': {'required': "Ce champ est obligatoire", },
        }
    def clean_num_solution(self):
            data = self.cleaned_data.get('num_solution')
            if not data > 0:
                raise forms.ValidationError(
                        "Le Numéro de solution doit etre positive.")
            return data
    def clean_description_solution(self):
            data = self.cleaned_data.get('description_solution')
            if not data.islower():
                raise forms.ValidationError("La description de réclamation devrait être en minuscule")
            if not validate_digits_letters_espace(data[0]) or "'" in data[0]:
                raise forms.ValidationError(
                    "La description de réclamationne doit pas commancer par des caractères spéciaux.")
                data.strip()
            return data


