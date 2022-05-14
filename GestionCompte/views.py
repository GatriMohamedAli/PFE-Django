from django.shortcuts import render, redirect

# Create your views here.
from pip._internal.utils import logging

from GestionCompte.forms import ResponsableForm, UtilisateurForm, ChefForm, ResponsableMagasinForm, FormConfirm
from GestionCompte.models import Administrateur
from GestionProjet.models import Chef_Projet, Responsable_Projet, Projet, DetailleAffectation
from GestionReclamation.models import Reclamation, Solution
from Magasin.models import Responsable_Magasin, Article
from general.models import Utilisateur
from django.db.models import Sum, Count, Q
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.core.mail import EmailMessage
from PFE.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import JsonResponse


def admin(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])
    responsable = Responsable_Projet.objects.all()
    responsable_total = responsable.count()

    chef_projet = Chef_Projet.objects.all()
    chef_projet_total = chef_projet.count()

    responsable_magasin = Responsable_Magasin.objects.all()
    responsable_magasin_total = responsable_magasin.count()

    context = {'administrateur': administrateur, 'responsable': responsable, 'responsable_total': responsable_total,
               'chef_projet': chef_projet, 'chef_projet_total': chef_projet_total, 'responsable_magasin': responsable_magasin,
               'responsable_magasin_total': responsable_magasin_total}
    return render(request, 'compte/Administrateur.html', context)


def liste_Utilisateur(request, choix):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])
    responsable = Responsable_Projet.objects.all()
    chef_projet = Chef_Projet.objects.all()
    responsable_magasin = Responsable_Magasin.objects.all()
    res = None
    if request.is_ajax():
        search = request.POST.get('s')
        print(search)
        arts = Utilisateur.objects.filter(role=choix)
        allofthem = []
        all = []
        for a in arts:
            al = {'id': a.id}
            all.append(al)
        print(all)
        art = arts.filter(
            Q(telephone__icontains=search) | Q(nom__icontains=search) | Q(prenom__icontains=search))
        """ print("filter ", articles) """
        data = []
        for ar in art:
            item = {'id': ar.id}
            data.append(item)
        allofthem.append(data)
        allofthem.append(all)
        res = allofthem
        return JsonResponse({'data': res})

    if choix == 'Responsable':
        print(responsable)
        context = {'administrateur': administrateur, 'responsables': responsable,
                   'chef_projet': chef_projet, 'responsable_magasin': responsable_magasin}
        return render(request, 'compte/liste_ResponsablesProjets.html', context)
    elif choix == 'chefProjet':
        context = {'administrateur': administrateur, 'responsable': responsable,
                   'chef_projet': chef_projet, 'responsable_magasin': responsable_magasin}
        return render(request, 'compte/liste_ChefProjet.html', context)

    else:
        context = {'administrateur': administrateur, 'responsable': responsable,
                   'chef_projet': chef_projet, 'responsable_magasin': responsable_magasin}
        return render(request, 'compte/liste_ResponsableMagasin.html', context)


def ajouter_utilisateur(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])
    Subject = 'Bienvenue à Tunisie Télécom'
    Message = 'Votre mot de passe est : '
    form = UtilisateurForm()
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['role'] == 'Responsable':
                choix = 'Responsable'
                form = ResponsableForm(request.POST, request.FILES or None)
                form.save()
                Message = Message+str(form['motDePasse'].value())
                send_mail(Subject, Message, EMAIL_HOST_USER, [
                          str(form['email'].value())], fail_silently=False)
                return redirect('liste_Utilisateur',  choix)
            elif form.cleaned_data['role'] == 'chefProjet':
                choix = 'chefProjet'
                form = ChefForm(request.POST, request.FILES or None)
                form.save()
                Message = Message+str(form['motDePasse'].value())
                send_mail(Subject, Message, EMAIL_HOST_USER, [
                          str(form['email'].value())], fail_silently=False)
                return redirect('liste_Utilisateur',  choix)
            elif form.cleaned_data['role'] == 'ResponsableMagasin':
                choix = 'ResponsableMagasin'
                form = ResponsableMagasinForm(
                    request.POST, request.FILES or None)
                form.save()
                Message = Message+str(form['motDePasse'].value())
                send_mail(Subject, Message, EMAIL_HOST_USER, [
                          str(form['email'].value())], fail_silently=False)
                return redirect('liste_Utilisateur', choix)
    context = {'administrateur': administrateur, 'form': form}
    return render(request, 'compte/ajouter_utilisateur.html', context)


def modifier_utilisateur(request, user):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])
    utilisateur = Utilisateur.objects.get(id=user)
    choix = utilisateur.role
    form = UtilisateurForm(instance=utilisateur)
    if request.method == 'POST':
        form = UtilisateurForm(
            request.POST, request.FILES or None, instance=utilisateur)
        if form.is_valid():
            form.save()
            return redirect('liste_Utilisateur', choix)
    context = {'form': form, 'administrateur': administrateur,
               'utilisateur': utilisateur}
    return render(request, 'compte/modifier_utilisateur.html', context)


def supprimer_utilisateur(request, user):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])
    utilisateur = Utilisateur.objects.get(id=user)
    if request.method == 'POST':
        utilisateur.delete()
        ch = '/Administrateur/'
        return redirect(ch)
    context = {'utilisateur': utilisateur, 'administrateur': administrateur}
    return render(request, 'compte/supprimer_utilisateur.html', context)


def profile_utilisateur(request):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'administrateur': administrateur}
        return render(request, 'compte/profile_utilisateur.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'responsable': responsable}
        return render(request, 'projet/responsable_projet/profile_utilisateur.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'chef_projet': chef_projet}
        return render(request, 'projet/chef_projet/profile_utilisateur.html', context)
    else:
        responsable = utilisateur
        context = {'responsable': responsable}
        return render(request, 'magasin/Responsable/profile_utilisateur.html', context)


def modifier_profile(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    form = UtilisateurForm(instance=utilisateur)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST or None,
                               request.FILES or None, instance=utilisateur)
        if form.is_valid():
            utilisateur.save()
            return redirect('profile_utilisateur')
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'form': form, 'administrateur': administrateur}
        return render(request, 'compte/modifier_profile.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable}
        return render(request, 'projet/responsable_projet/modifier_profile.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'form': form, 'chef_projet': chef_projet}
        return render(request, 'projet/chef_projet/modifier_profile.html', context)
    else:
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable}
        return render(request, 'magasin/Responsable/modifier_profile.html', context)


def modifier_passe(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    form = FormConfirm(request.POST, request.FILES or None)
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    message = ""
    if request.method == 'POST':
        form = FormConfirm(request.POST)
        if form.is_valid():
            if form['motDePasse'].value() == utilisateur.motDePasse:
                if form['new_password'].value() == form['confirm_password'].value():
                    utilisateur.motDePasse = form['confirm_password'].value()
                    utilisateur.save()
                    return redirect('profile_utilisateur')
            else:
                message = "Mots de passe incorrect"
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'message': message, 'form': form,
                   'administrateur': administrateur}
        return render(request, 'compte/modifier_passe.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'message': message, 'form': form,
                   'responsable': responsable}
        return render(request, 'projet/responsable_projet/modifier_passe.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'message': message, 'form': form,
                   'chef_projet': chef_projet}
        return render(request, 'projet/chef_projet/modifier_passe.html', context)
    else:
        responsable = utilisateur
        context = {'message': message, 'form': form,
                   'responsable': responsable}
        return render(request, 'magasin/Responsable/modifier_passe.html', context)


def statProj(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])

    responsable = Responsable_Projet.objects.all()
    responsable_total = responsable.count()

    chef_projet = Chef_Projet.objects.all()
    chef_projet_total = chef_projet.count()

    nbrA = Projet.objects.filter(etat_projet="a faire")
    nbrAfaire = nbrA.count()
    nbrT = Projet.objects.filter(etat_projet="terminé")
    nbrEncours = nbrT.count()
    nbrE = Projet.objects.filter(etat_projet="en cours")
    nbrTermine = nbrE.count()
    datapie = [nbrAfaire, nbrEncours, nbrTermine]
    mylistchefs = []
    mylistproj = []
    chefs = Utilisateur.objects.filter(role="chefProjet")
    for chef in chefs:
        projets = Projet.objects.filter(chef_projet=chef.id)
        mylistchefs.append(chef.prenom)
        mylistproj.append(projets.count())

    responsable_magasin = Responsable_Magasin.objects.all()
    responsable_magasin_total = responsable_magasin.count()

    context = {'administrateur': administrateur, 'responsable': responsable, 'responsable_total': responsable_total,
               'chef_projet': chef_projet, 'chef_projet_total': chef_projet_total, 'responsable_magasin': responsable_magasin,
               'responsable_magasin_total': responsable_magasin_total, 'datapie': datapie, 'listchef': mylistchefs, 'listporj': mylistproj}
    return render(request, 'compte/statAdmin.html', context)


def statMag(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])

    responsable = Responsable_Projet.objects.all()
    responsable_total = responsable.count()

    chef_projet = Chef_Projet.objects.all()
    chef_projet_total = chef_projet.count()

    listart = []
    datapie = []
    Arts = Article.objects.all()

    for art in Arts:
        listart.append(art.code_article)
        datapie.append(art.dispo_article)

    responsable_magasin = Responsable_Magasin.objects.all()
    responsable_magasin_total = responsable_magasin.count()
    arr = Article.objects.all()
    arrTotal = arr.count()

    listartid = []
    listartnbr = []
    Proj = DetailleAffectation.objects.all()

    for proj in Proj:
        if proj.article_id in listartid:
            ind = listartid.index(proj.article_id)
            listartnbr[ind] = listartnbr[ind]+proj.nombre
        else:
            listartid.append(proj.article_id)
            listartnbr.append(proj.nombre)

    for count, idd in enumerate(listartid):
        a = Article.objects.get(id=idd)
        listartid[count] = a.code_article

    projart = DetailleAffectation.objects.values('date_ajout') \
        .annotate(somme=Sum('nombre')) \
        .order_by('date_ajout')
    datelist = []
    nbrlist = []
    for p in projart:
        thedate = p["date_ajout"].strftime("%b-%y")
        datelist.append(thedate)
        nbrlist.append(p["somme"])

    context = {'administrateur': administrateur,
               'arrTotal': arrTotal, 'responsable_magasin': responsable_magasin,
               'responsable_magasin_total': responsable_magasin_total, 'datapie': datapie, 'listart': listart, 'listartid': listartid, 'listartnbr': listartnbr, 'datelist': datelist, 'nbrlist': nbrlist}
    return render(request, 'compte/statAdminMagasin.html', context)


def statRec(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'admin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    administrateur = Administrateur.objects.get(id=request.session['id'])

    reclamation = Reclamation.objects.all()
    reclamation_total = reclamation.count()

    # PIE
    nbrA = Reclamation.objects.filter(statut="en attente")
    nbrAtt = nbrA.count()
    nbrT = Reclamation.objects.filter(statut="prise en charge")
    nbrPrise = nbrT.count()
    nbrE = Reclamation.objects.filter(statut="en traitement")
    nbrTrait = nbrE.count()
    nbrE = Reclamation.objects.filter(statut="terminé")
    nbrTermine = nbrE.count()
    datapie = [nbrAtt, nbrPrise, nbrTrait, nbrTermine]
    data = ["en attente", "prise en charge", "en traitement", "terminé"]

    # BAR
    rec = Reclamation.objects.values('service')
    listrec = []
    listrecnbr = []
    for r in rec:
        if not r["service"] in listrec:
            lesrecs = Reclamation.objects.filter(service=r["service"])
            nbrrec = lesrecs.count()
            listrec.append(r["service"])
            listrecnbr.append(nbrrec)

    # LINE
    alldate = Reclamation.objects.values(
        'date_creation').order_by('date_creation')
    listdateall = []
    for d in alldate:
        thed = d["date_creation"].strftime("%b-%y")
        if not thed in listdateall:
            listdateall.append(thed)

    # PROJET
    recspec = Reclamation.objects.values('date_creation') \
        .filter(service="Projet") \
        .annotate(somme=Count('service')) \
        .order_by('date_creation')

    datelistProj = []
    nbrlistProj = []
    for p in recspec:
        thedate = p["date_creation"].strftime("%b-%y")
        if not thedate in datelistProj:
            datelistProj.append(thedate)
            nbrlistProj.append(p["somme"])
        else:
            nbrlistProj[datelistProj.index(
                thedate)] = nbrlistProj[datelistProj.index(thedate)]+1

    # MAG
    recMag = Reclamation.objects.values('date_creation') \
        .filter(service="Magasin") \
        .annotate(somme=Count('service')) \
        .order_by('date_creation')

    datelistMag = []
    nbrlistMag = []
    for p in recMag:
        thedate = p["date_creation"].strftime("%b-%y")
        datelistMag.append(thedate)
        nbrlistMag.append(p["somme"])

    # RH
    recRH = Reclamation.objects.values('date_creation') \
        .filter(service="RH") \
        .annotate(somme=Count('service')) \
        .order_by('date_creation')

    datelistRH = []
    nbrlistRH = []
    for p in recRH:
        thedate = p["date_creation"].strftime("%b-%y")
        datelistRH.append(thedate)
        nbrlistRH.append(p["somme"])

    # IT
    recIT = Reclamation.objects.values('date_creation') \
        .filter(service="IT") \
        .annotate(somme=Count('service')) \
        .order_by('date_creation')

    datelistIT = []
    nbrlistIT = []
    for p in recIT:
        thedate = p["date_creation"].strftime("%b-%y")
        datelistIT.append(thedate)
        nbrlistIT.append(p["somme"])

    for count, d in enumerate(listdateall):
        if not d in datelistMag:
            nbrlistMag.insert(count, 0)
        if not d in datelistProj:
            nbrlistProj.insert(count, 0)
        if not d in datelistRH:
            nbrlistRH.insert(count, 0)
        if not d in datelistIT:
            nbrlistIT.insert(count, 0)

    print(recspec)
    print("date list MAG", datelistMag)
    print("list DATE PROJ", datelistProj)
    print("list NBR PROJ", nbrlistProj)
    print("date list ALL", listdateall)
    print("list NBR MAG", nbrlistMag)
    print(recMag)

    # AJAX
    if request.is_ajax():
        data = request.POST.get("data")
        recl = Reclamation.objects.filter(service=data)
        print("recla par dep ", recl)
        ttrecl = []
        ttsolu = []
        for r in recl:
            ttrecl.append(r.objet)
            solu = Solution.objects.filter(reclamation=r)
            x = solu.count()
            ttsolu.append(x)

        nbrA = Reclamation.objects.filter(
            service=data).filter(statut="en attente")
        nbrAtt = nbrA.count()
        nbrT = Reclamation.objects.filter(
            service=data).filter(statut="prise en charge")
        nbrPrise = nbrT.count()
        nbrE = Reclamation.objects.filter(
            service=data).filter(statut="en traitement")
        nbrTrait = nbrE.count()
        nbrE = Reclamation.objects.filter(
            service=data).filter(statut="terminé")
        nbrTermine = nbrE.count()
        datapie = [nbrAtt, nbrPrise, nbrTrait, nbrTermine]
        return JsonResponse({'data': ttsolu, 'ttrecl': ttrecl, 'datapie': datapie})

    context = {'administrateur': administrateur, 'reclamation_total': reclamation_total,
               'listrec': listrec, 'listrecnbr': listrecnbr, 'data': data, 'datapie': datapie,
               'nbrlistproj': nbrlistProj, 'nbrlistmag': nbrlistMag,
               'nbrlistrh': nbrlistRH, 'nbrlistit': nbrlistIT,
               'alldate': listdateall}
    return render(request, 'compte/statAdminRec.html', context)
