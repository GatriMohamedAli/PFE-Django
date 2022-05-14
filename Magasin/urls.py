from django.contrib import admin
from django.urls import path
from Magasin import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
urlpatterns = [
    path('ResponsableMagasin/articles',
         views.article_list, name="article_list"),
    path('ResponsableMagasin/commander',
         views.commander, name="commander"),
    path('ResponsableMagasin/stat', views.statMag, name="stat"),
    path('ResponsableMagasin/edit/<str:comm>',
         views.editcomm, name="editcomm"),
    path('ResponsableMagasin/articles/create/',
         views.article_create, name='article_create'),
    path('ResponsableMagasin/articles/<id>/update/',
         views.article_update, name='article_update'),
    path('ResponsableMagasin/articles/<id>/delete/',
         views.article_delete, name='article_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
