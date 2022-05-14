from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('Administrateur/', views.admin, name='Administrateur'),
    path('Administrateur/StatProj',
         views.statProj, name='statProj'),
    path('Administrateur/StatMag',
         views.statMag, name='statMag'),
    path('Administrateur/StatRec',
         views.statRec, name='statRec'),
    path('Administrateur/liste_Utilisateur/<str:choix>',
         views.liste_Utilisateur, name='liste_Utilisateur'),
    path('Administrateur/ajouter_utilisateur',
         views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('Administrateur/supprimer_utilisateur/<int:user>',
         views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('Administrateur/modifier_utilisateur/<int:user>',
         views.modifier_utilisateur, name='modifier_utilisateur'),
    path('profile_utilisateur',
         views.profile_utilisateur, name='profile_utilisateur'),
    path('modifier_profile',
         views.modifier_profile, name='modifier_profile'),
    path('modifier_passe', views.modifier_passe, name='modifier_passe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
