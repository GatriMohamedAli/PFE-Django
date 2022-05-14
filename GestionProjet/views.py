import calendar

from django.core.mail.backends import console
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from future.backports.datetime import timedelta

from GestionReclamation.models import Reclamation
from .filters import ProjetFiltre
# Create your views here.
from django.template.loader import get_template
import json
from django.views import View
from .forms import ProjetForm, ItemForm, ArticleAdd, etatForm, tacheUpdateFrom
from .models import Projet, Chef_Projet, DetailleAffectation, Utilisateur, Responsable_Projet, Tache
from Magasin.models import Article

import _datetime
from .utils import render_to_pdf
from .forms import tacheFrom
from django.db.models import Q, Sum

from datetime import datetime, date


from datetime import datetime
from django.http import HttpResponse, JsonResponse

from .models import *
from general.models import Utilisateur


def home(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    responsable = Responsable_Projet.objects.get(id=request.session['id'])
    projets = Projet.objects.all()
    chefs = Chef_Projet.objects.all()
    projets_total = projets.count()
    chefs_total = chefs.count()
    responsables = Responsable_Projet.objects.all()
    responsable_total = responsables.count()
    listeProjetsDeMois = Projet.objects.filter(
        date_debut__month__gte=date.today().month)
    print(listeProjetsDeMois)
    reclamations_envoyee = Reclamation.objects.filter(
        service='Projet', statut='en attente')

    if request.is_ajax():
        idproj = request.POST.get('data')
        proj = Projet.objects.get(id=idproj)
        item = {
            'nom': proj.nom_projet,
            'desc': proj.description_projet,
            'cara': proj.caracteristique_projet
        }
        return JsonResponse({"res": item})

    context = {'projets': projets, 'projets_total': projets_total, 'chefs_total': chefs_total,
               'responsable': responsable, 'responsable_total': responsable_total,
               'listeProjetsDeMois': listeProjetsDeMois, 'reclamations_envoyee': reclamations_envoyee, 'chefs': chefs}
    return render(request, 'projet/responsable_projet/acceuil.html', context)


def ajouter_projet(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Projet.objects.get(id=request.session['id'])
    form = ProjetForm()
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.save()
            ch = '/Responsable1/liste_Projet'
            return redirect(ch)
    context = {'form': form, 'responsable': responsable}
    return render(request, 'projet/responsable_projet/ajouter_projet.html', context)


def modifier_projet(request, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Projet.objects.get(id=request.session['id'])
    projet = Projet.objects.get(id=proj)
    form = ProjetForm(instance=projet)
    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            ch = '/Responsable1/liste_Projet'
            return redirect(ch)
    context = {'form': form, projet: 'projet', 'responsable': responsable}
    return render(request, 'projet/responsable_projet/modifier_projet.html', context)


def supprimer_projet(request, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Projet.objects.get(id=request.session['id'])
    projet = Projet.objects.get(id=proj)
    tache = projet.tache_set.all()
    all_tache = tache.count()
    message = "Voulez-vous supprimer le projet ?"
    if request.method == 'POST':
        if all_tache < 1:
            projet.delete()
            ch = '/Responsable1/liste_Projet'
            return redirect(ch)
        else:
            message = "il faux supprimer les tâche avant la supprission de projet"
    context = {'item': projet, 'responsable': responsable,
               'projet': projet, 'message': message}
    return render(request, 'projet/responsable_projet/supprimer_projet.html', context)


def listprojet(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Projet.objects.get(id=request.session['id'])

    if request.is_ajax():
        idproj = request.POST.get('data')
        proj = Projet.objects.get(id=idproj)
        item = {
            'nom': proj.nom_projet,
            'desc': proj.description_projet,
            'cara': proj.caracteristique_projet
        }
        return JsonResponse({"res": item})

    projets = Projet.objects.all()
    chefs = Chef_Projet.objects.all()

    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['id']

        cmd = get_object_or_404(Projet, id=content)
        tache = cmd.tache_set.all()
        all_tache = tache.count()
        test = False
        if all_tache < 1:
            cmd.delete()
            test = True

        return JsonResponse({"test": test})

    context = {'projets': projets, 'responsable': responsable, 'chefs': chefs}
    return render(request, 'projet/responsable_projet/list_projet.html', context)


def listeChef(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Projet.objects.get(id=request.session['id'])
    chefs = Chef_Projet.objects.all()
    res = None
    if request.is_ajax():
        search = request.POST.get('s')
        print(search)
        arts = Utilisateur.objects.filter(role="chefProjet")
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
    context = {'chefs': chefs, 'responsable': responsable}
    return render(request, 'projet/responsable_projet/list_chef.html', context)


# chef_projet


def list_projet(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef_projet = Chef_Projet.objects.get(id=request.session['id'])
    if request.is_ajax():
        idproj = request.POST.get('data')
        proj = Projet.objects.get(id=idproj)
        item = {
            'nom': proj.nom_projet,
            'desc': proj.description_projet,
            'cara': proj.caracteristique_projet
        }
        return JsonResponse({"res": item})
    projet = chef_projet.projet_set.all()
    projet_total = projet.count()
    myFilter = ProjetFiltre(request.GET, queryset=projet)
    projet = myFilter.qs
    context = {'chef_projet': chef_projet, 'projet': projet,
               'projet_total': projet_total, 'myFilter': myFilter}
    return render(request, 'projet/chef_projet/liste_projets.html', context)


def ajouter_article(request, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef_projet = Chef_Projet.objects.get(id=request.session['id'])
    projet = Projet.objects.get(id=proj)
    articles = Article.objects.exclude(id=111111111)

    res = None
    if request.is_ajax():
        search = request.POST.get('s')
        print(search)
        arts = Article.objects.exclude(id=1111111111)
        allofthem = []
        all = []
        for a in arts:
            al = {'id': a.id}
            all.append(al)
        print(all)
        art = Article.objects.filter(
            Q(code_article__icontains=search) | Q(categorie__icontains=search))
        print("filter ", articles)
        data = []
        for ar in art:
            item = {'id': ar.id}
            data.append(item)
        allofthem.append(data)
        allofthem.append(all)
        res = allofthem
        return JsonResponse({'data': res})

    context = {'article': articles,
               'projet': projet, 'chef_projet': chef_projet}
    return render(request, 'projet/chef_projet/ajouter_article.html', context)


def ajouter_article2(request, arti, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])

    articles = Article.objects.get(code_article=arti)
    projet = Projet.objects.get(id=proj)

    context = {'art': articles, 'projet': projet, 'chef_projet': chef}
    return render(request, 'projet/chef_projet/ajouter_article2.html', context)


def comfirmer_article(request,  arti, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])

    projet = Projet.objects.get(id=proj)

    articles = Article.objects.get(code_article=arti)
    num = request.POST.get('number')
    if articles.dispo_article >= int(num):
        test = True
        projarti = DetailleAffectation()
        projarti.article = articles
        projarti.projet = Projet.objects.get(id=proj)
        projarti.chef_projet = Chef_Projet.objects.get(
            id=request.session['id'])
        projarti.nombre = int(num)
        projarti.date_ajout = _datetime.date.today()
        projarti.save()
        art = Article.objects.get(code_article=arti)
        art.dispo_article = art.dispo_article-int(num)
        art.save()
        return redirect('listeArticleProjet', proj)
    else:
        test = False
    context = {'art': articles, 'projet': projet,
               'chef_projet': chef, 'test': test}
    return render(request, 'projet/chef_projet/ajouter_article2.html', context)


def listeArticleProjet(request, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])

    projet = Projet.objects.get(id=proj)
    listeProjets = DetailleAffectation.objects.filter(projet_id=projet).order_by(
        'article_id').values_list('article_id', flat=True).distinct()
    liste = [Article.objects.get(id=x) for x in listeProjets]
    print(liste)
    listeNombre = [sum(DetailleAffectation.objects.filter(article_id=x).filter(
        projet_id=projet).values_list('nombre', flat=True))for x in listeProjets]
    print(listeNombre)
    mylist = [(liste[i], listeNombre[i]) for i in range(len(liste))]
    print(mylist[0][0])

    context = {'chef_projet': chef, 'projet': projet, 'mylist': mylist}
    return render(request, 'projet/chef_projet/listeArticleProjet.html', context)


def detaille_projet(request,  proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])
    projet = Projet.objects.get(id=proj)

    tache = projet.tache_set.all()

    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['id']

        cmd = get_object_or_404(Tache, id=content)
        cmd.delete()

    if request.is_ajax():
        idr = request.POST.get('data')
        tache = Tache.objects.get(id=idr)
        item = {
            'nom': tache.titre_tache,
            'desc': tache.description_tache,
            'dem': tache.demarche_tache,
            'diff': tache.difficulté_tache

        }
        return JsonResponse({"res": item})

    context = {'projet': projet, 'chef_projet': chef, 'tache': tache}
    return render(request, 'projet/chef_projet/detaille_projet.html', context)


def terminer_projet(request, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])
    projet = Projet.objects.get(id=proj)
    proj = chef.projet_set.all()
    projet.etat_projet = "terminé"
    projet.save()
    context = {'chef_projet': chef, 'projet': proj}
    return render(request, 'projet/chef_projet/liste_projets.html', context)


def search_Tache(request):
    if request.is_ajax():
        res = None
        tache = request.POST.get('titre')
        desc = request.POST.get('desc')
        if desc == None:
            desc = ""
        if tache == None:
            tache = ""
        print('tache ==', tache)
        qs = Tache.objects.filter(Q(titre_tache__icontains=tache))
        if len(qs) > 0 and len(tache) > 0:
            data = []
            for pos in qs:
                item = {
                    'id': pos.id,
                    'Titre': pos.titre_tache,
                    'description_tache': pos.description_tache,

                }
                data.append(item)
            res = data
        else:
            res = 'Aucune Tâche trouvée...'
        return JsonResponse({'data': res})
    return JsonResponse({})


def ajout_tache(request,  proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    if request.is_ajax():
        print(request.POST.get('name'))
        if request.POST.get('name') == 'ADD':
            print("Ajax sent")
            res = 1
            param = request.POST.get('idtache')
            print(param)
            tache = Tache.objects.get(id=param)
            tach = Tache()
            tach.titre_tache = tache.titre_tache
            tach.description_tache = tache.description_tache
            tach.mots_clés = tache.mots_clés
            tach.demarche_tache = tache.demarche_tache
            tach.difficulté_tache = tache.difficulté_tache
            tach.projet = Projet.objects.get(id=proj)
            if tach.save():
                res = 0
            return JsonResponse({'res': res})
        if request.POST.get('name') == 'view':
            print('VIEW RQST SENT')
            param = request.POST.get('idtache')
            print(param)
            tache = Tache.objects.get(id=param)
            item = {
                'titre': tache.titre_tache,
                'desc': tache.description_tache,
                'cle': tache.mots_clés,
                'demarche': tache.demarche_tache,
                'diff': tache.difficulté_tache
            }
            return JsonResponse({'res': item})

    chef = Chef_Projet.objects.get(id=request.session['id'])
    form = tacheFrom()
    projet = Projet.objects.get(id=proj)
    print(form)
    if request.method == 'POST':
        form = tacheFrom(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('detaille_projet', proj)
    context = {'form': form, 'projet': projet, 'chef_projet': chef}
    return render(request, 'projet/chef_projet/ajout_tache.html', context)


def modifier_tache(request, tache, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])

    tache = Tache.objects.get(id=tache)
    projet = Projet.objects.get(id=proj)
    form = tacheUpdateFrom(instance=tache)
    if request.method == 'POST':
        form = tacheUpdateFrom(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            ch = '/chefProjet/detaille_projet/' + proj
            return redirect(ch)
    context = {'form': form, 'projet': projet,
               'tache': tache, 'chef_projet': chef}
    return render(request, 'projet/chef_projet/modifier_tache.html', context)


def supprimer_tache(request,  tache, proj):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'chefProjet':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    chef = Chef_Projet.objects.get(id=request.session['id'])
    tache = Tache.objects.get(id=tache)
    projet = Projet.objects.get(id=proj)
    if request.method == 'POST':
        tache.delete()
        ch = '/chefProjet/detaille_projet/' + proj
        return redirect(ch)
    context = {'projet': projet, 'tache': tache, 'chef_projet': chef}
    return render(request, 'projet/chef_projet/supprimer_tache.html', context)


class GeneratePdf(View):
    def get(self, request, pk, **kwargs):
        template = get_template('projet/chef_projet/pdf_detail.html')
        projet = Projet.objects.get(id=pk)
        tache = projet.tache_set.all()
        print(tache)
        context = {'projet': projet, 'tache': tache}
        html = template.render(context)
        pdf = render_to_pdf('projet/chef_projet/pdf_detail.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def statProj(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'Responsable':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    responsable = Responsable_Projet.objects.get(id=request.session['id'])

    responsables = Responsable_Projet.objects.all()
    responsable_total = responsables.count()
    projets = Projet.objects.all()
    projets_total = projets.count()
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

    context = {'responsable': responsable, 'responsable_total': responsable_total,
               'chef_projet': chef_projet, 'chef_projet_total': chef_projet_total,
               'datapie': datapie, 'listchef': mylistchefs, 'listporj': mylistproj, 'projets_total': projets_total}
    return render(request, 'projet/responsable_projet/stat.html', context)
