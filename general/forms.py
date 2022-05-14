from django import forms
class Subscribe(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control',
            'placeholder': ('seuemail@email.com'),
            'required': 'required'
        }),
        error_messages={'invalid': 'veuillez respecter le format email :seuemail@email.com ',
                        'required': "Ce champ est obligatoire"})