from django.contrib.auth import logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import Subscribe
from .models import Utilisateur
from django.core.mail import EmailMessage
from random import randint
from django.shortcuts import render
from PFE.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True)
def user_login(request):
    request.session.modified = True
    try:
        del request.session['id']

    except:
        pass
    if request.POST:
        try:
            email = request.POST.get('email')
            motDePasse = request.POST.get('motDePasse')
            utilisateur = Utilisateur.objects.get(email=email)
            if utilisateur is not None:
                if utilisateur.motDePasse == motDePasse:
                    if utilisateur.role == 'admin':
                        request.session['id'] = utilisateur.id
                        ch = '/Administrateur/'
                        administrateur = utilisateur.id
                        context = {'administrateur': administrateur}
                        return redirect(ch, context)

                    if utilisateur.role == 'Responsable':
                        request.session['id'] = utilisateur.id
                        ch = '/accueil_Responsable/'
                        responsable = utilisateur.id
                        context = {'responsable': responsable}
                        return redirect(ch, context)

                    if utilisateur.role == 'chefProjet':
                        request.session['id'] = utilisateur.id
                        ch = '/chef_projet/'
                        chef_projet = utilisateur.id
                        context = {'chef_projet': chef_projet}
                        return redirect('chef_projet')

                    if utilisateur.role == 'ResponsableMagasin':
                        request.session['id'] = utilisateur.id
                        responsable = utilisateur.id
                        context = {'responsable': responsable}
                        ch = '/ResponsableMagasin/articles'
                        return redirect(ch, context)

                if utilisateur.motDePasse != motDePasse:
                    message = "mot de passe incorrect !! "
                    context = {'message': message}
                    return render(request, 'login.html', context)
        except ObjectDoesNotExist:
            utilisateur = None
            message = "Email est  incorrect !! "
            context = {'message': message}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.modified = True
    try:
        del request.session['id']

    except:
        return redirect('login')
    return redirect('login')


def subscribe(request):
    form = Subscribe(request.POST)
    code = randint(25879, 74562)
    request.session['code'] = code
    ch = ""
    if request.method == "POST":
        if form.is_valid():
            subject = 'Bienvenue dans le projet Tunisie Télécom'
            message = str(code)+' : votre code de validation Email '
            recepient = str(form['email'].value())
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient], fail_silently=False)
            return redirect('valider', email=form['email'].value())
        else:
            ch = "Email est  incorrect !! "
    return render(request, 'subscribe/index.html', {'form': form, 'ch': ch})


def valider(request, email):
    request.session.modified = True
    code = request.session['code']

    if request.method == "POST":
        verif = request.POST.get('code')
        if int(verif) == code:
            try:
                del request.session['code']
            except:
                pass

            return redirect('success', email=email)

    return render(request, 'subscribe/valider.html')


def success(request, email):
    request.session.modified = True
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    message = ""
    if request.POST:
        if new_password == confirm_password:
            utilisateur = Utilisateur.objects.get(email=email)
            utilisateur.motDePasse = new_password
            utilisateur.save()
            return redirect('login')
        else:
            message = "mots de passe invalid"
    context = {'message': message}
    return render(request, 'subscribe/success.html', context)
