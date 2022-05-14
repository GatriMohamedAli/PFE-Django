from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path
from . import views
urlpatterns = [
    path('accueil_Responsable/', views.home, name='acceuil'),

    path('searchtache/', views.search_Tache,name='searchTache'),
    path('Responsable1/listeChef', views.listeChef, name='chefs'),
    path('Responsable1/stat', views.statProj, name='statproj'),
    path('Responsable1/liste_Projet',
         views.listprojet, name='liste_Projet'),

    path('Responsable1/ajout_projet/',
         views.ajouter_projet, name='ajout_projet'),

    path('Responsable1/modifier_projet/<proj>',
         views.modifier_projet, name='modifier_projet'),
         
    path('Responsable1/supprimer_projet/<proj>',
         views.supprimer_projet, name='supprimer_projet'),

    path('chefProjet/detaille_projet/<int:proj>',
         views.detaille_projet, name='detaille_projet'),

    path('chefProjet/ajout_tache/<proj>',
         views.ajout_tache, name='ajout_tache'),

    path('chefProjet/terminer_projet/<proj>',
         views.terminer_projet, name='terminer_projet'),

    path('chefProjet/detaille_projet/<proj>/modifier_tache/<tache>',
         views.modifier_tache, name='modifier_tache'),

    path('chefProjet/detaille_projet/<proj>/supprimer_tache/<tache>',
         views.supprimer_tache, name='supprimer_tache'),

    path('chefProjet/', views.list_projet, name='chef_projet'),

    path('chefProjet/ajouterArticle/<proj>',
         views.ajouter_article, name='ajouter_article'),

    path('chefProjet/ajouterArticle2/<proj>/<arti>',
         views.ajouter_article2, name='ajouter_article2'),

    path('chefProjet/comfirmer_article/<proj>/<arti>',
         views.comfirmer_article, name='comfirmer_article'),

    path('chefProjet/listeArticleProjet/<str:proj>/',views.listeArticleProjet, name='listeArticleProjet'),

    path('pdf/<str:pk>', views.GeneratePdf.as_view(), name='pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
