from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout', views.logout, name='logout'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('valider/<email>', views.valider, name='valider'),
    path('success/<email>/', views.success, name='success'),

]
