from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
urlpatterns = [

    path('search/', views.search_results, name='search'),
    path('search_solution/', views.search_results_solution, name='search_solution'),

    path('TreminerReclamation/<str:rec>',
         views.TreminerReclamation, name='TreminerReclamation'),
    path('TraitementReclamation/<str:rec>',
         views.TraitementReclamation, name='TraitementReclamation'),
    path('listReclamation/', views.listReclamation, name='listReclamation'),
    path('ajouterReclamation/', views.ajouterReclamation,
         name='ajouterReclamation'),
    path('supprimerReclamation/<str:reclamations>',
         views.supprimerReclamation, name='supprimerReclamation'),
    path('modifierReclamation/<str:reclamations>',
         views.modifierReclamation, name='modifierReclamation'),


    path('listSolutionReclamation/<str:rec>',
         views.listSolutionReclamation, name='listSolutionReclamation'),
    path('ajouterSolution/<str:rec>',
         views.ajouterSolutionReclamation, name='ajouterSolution'),
    path('solutionDétailler/<str:rec>/detaille/<str:sol>',
         views.detaille, name='detaille'),
    path('<str:rec>/supprimerSolution/<str:sol>',
         views.supprimerSolution, name='supprimerSolution'),
    path('listSolutionReclamation/<str:rec>/modifierSolution/<str:sol>',
         views.modifierSolution, name='modifierSolution'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
