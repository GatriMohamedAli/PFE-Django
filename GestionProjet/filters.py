import django_filters
from .models import Projet
class ProjetFiltre(django_filters.FilterSet):
    class Meta:
        model=Projet
        fields='__all__'
        exclude=['nom_projet','description_projet','adresse_projet','date_ajout_projet','date_debut','caracteristique_projet','chef_projet','date_fin']