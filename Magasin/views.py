from django.shortcuts import render, redirect, get_object_or_404
from Magasin.models import Article, Responsable_Magasin, Commande, Constituer
from Magasin.forms import CommandeAdd
from django.http import JsonResponse, HttpResponseRedirect
from general.models import Utilisateur
from django.template.loader import render_to_string

from Magasin.forms import ArticleAdd
from GestionProjet.models import Chef_Projet, Responsable_Projet, Projet, DetailleAffectation

from django.db.models import Sum, Count, Q
from datetime import datetime
import json
import logging
# Create your views here.


def article_list(request):
    try:
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    responsable = Responsable_Magasin.objects.get(id=request.session['id'])
    articles = Article.objects.exclude(id=1111111111)

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

        data = []
        for ar in art:
            item = {'id': ar.id}
            data.append(item)
        allofthem.append(data)
        allofthem.append(all)
        res = allofthem
        return JsonResponse({'data': res})

    context = {"articles": articles, "responsable": responsable}
    return render(request, 'magasin/Responsable/article_list.html', context)


def save_all(request, form, template_name):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            articles = Article.objects.exclude(id=1111111111)
            data['article_list'] = render_to_string(
                'magasin/Responsable/article_list_2.html', {'articles': articles})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def article_create(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    if request.method == 'POST':
        form = ArticleAdd(request.POST, request.FILES or None)
    else:
        form = ArticleAdd()
    return save_all(request, form, 'magasin/Responsable/ajouter_article.html')


def article_update(request, id):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        form = ArticleAdd(
            request.POST, request.FILES or None, instance=article)
    else:
        form = ArticleAdd(instance=article)
    return save_all(request, form, 'magasin/Responsable/modifier_article.html')


def article_delete(request, id):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    data = dict()
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.delete()
        data['form_is_valid'] = True
        articles = Article.objects.all()
        data['article_list'] = render_to_string(
            'magasin/Responsable/article_list_2.html', {'articles': articles})
    else:
        context = {'article': article}
        data['html_form'] = render_to_string(
            'magasin/Responsable/supprimer_article.html', context, request=request)

    return JsonResponse(data)


def commander(request):
    try:
        print("magason")
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Magasin.objects.get(id=request.session['id'])
    articles = Article.objects.exclude(id=1111111111)

    cmds = Commande.objects.all()
    form = CommandeAdd()
    link = '/ResponsableMagasin/commander'

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        adr = body['adresse']
        cmt = body['commentaire']
        liste = body['liste[]']
        ch = ""
        arts = []
        cmd = Commande()
        cmd.mail = responsable.email
        cmd.telephone = responsable.telephone
        cmd.adresse = adr
        cmd.status = "Pending"
        cmd.commentaire = cmt
        cmd.save()
        for i in liste:
            tab = i.split("*")
            const = Constituer()
            print("Code", tab[0])
            if Article.objects.filter(code_article=tab[0]).count() > 0:
                const.commande = Commande.objects.get(id=cmd.id)
                const.article = Article.objects.get(code_article=tab[0])
                const.qte = tab[1]
                const.save()
            else:
                const.commande = Commande.objects.get(id=cmd.id)
                const.article = Article.objects.get(id=1111111111)
                const.qte = int(tab[1])
                const.codeUnique = tab[0]
                const.save()

        print("IDDDD", cmd.id)

    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['id']

        cmd = get_object_or_404(Commande, id=content)
        cmd.delete()
        return redirect(link)

    print(cmds)
    context = {"cmds": cmds, "form": form, "responsable": responsable}
    return render(request, 'magasin/Responsable/commander.html', context)


def editcomm(request, comm):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Magasin.objects.get(id=request.session['id'])
    cmd = Commande.objects.get(id=comm)
    cmdd = Constituer.objects.filter(commande=comm)

    liste = []
    for c in cmdd:
        if c.article_id == 1111111111:
            liste.append(str(c.codeUnique)+"*"+str(c.qte))
        else:
            art = Article.objects.get(id=c.article_id)
            liste.append(art.code_article+"*"+str(c.qte))

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        adr = body['adresse']
        cmt = body['commentaire']
        stat = body['status']
        liste = body['liste[]']

        cmd.adresse = adr
        cmd.status = stat
        cmd.commentaire = cmt

        cmd.save()

        const = Constituer.objects.filter(commande=comm)
        listebase = []
        for con in const:
            if con.article_id == 1111111111:
                listebase.append(con.codeUnique+'*'+str(con.qte))
            else:
                art = Article.objects.get(id=con.article_id)
                listebase.append(art.code_article+"*"+str(con.qte))
        print(listebase)
        for l in listebase:
            tab = l.split("*")
            test = False
            for i in liste:
                tab1 = i.split("*")
                if tab[0] == tab1[0]:
                    test = True
            if test == False:
                if Article.objects.filter(code_article=tab[0]).exists():
                    art = Article.objects.get(code_article=tab[0])
                    const = Constituer.objects.get(
                        commande=comm, article=art.id)
                    const.delete()
                else:
                    const = Constituer.objects.get(
                        commande=comm, codeUnique=tab[0])
                    const.delete()

        for i in liste:
            t = i.split("*")
            if Article.objects.filter(code_article=t[0]).exists():
                art = Article.objects.get(code_article=t[0])
                if Constituer.objects.filter(commande=comm, article=art.id):
                    const = Constituer.objects.get(
                        commande=comm, article=art.id)
                    const.qte = int(t[1])
                    const.save()
                else:
                    const = Constituer()
                    const.article = art
                    const.commande = Commande.objects.get(id=comm)
                    const.qte = int(t[1])
                    const.codeUnique = t[0]
                    const.save()
            else:
                if Constituer.objects.filter(commande=comm, codeUnique=t[0]):
                    const = Constituer.objects.get(
                        commande=comm, codeUnique=t[0])
                    const.qte = int(t[1])
                    const.save()
                else:
                    const = Constituer()
                    const.article = Article.objects.get(id=1111111111)
                    const.commande = Commande.objects.get(id=comm)
                    const.codeUnique = t[0]
                    const.qte = int(t[1])
                    const.save()

        link = '/ResponsableMagasin/commander'

    context = {"cmd": cmd, "liste": liste, "responsable": responsable}
    return render(request, 'magasin/Responsable/editcomm.html', context)


def statMag(request):
    try:
        print(request.session['id'])
        if request.session['id']:
            usertest = Utilisateur.objects.get(id=request.session['id'])
            if not usertest.role == 'ResponsableMagasin':
                return render(request, 'ErrorRole.html')
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')

    responsable = Responsable_Magasin.objects.get(id=request.session['id'])

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

    context = {'responsable': responsable,
               'arrTotal': arrTotal, 'responsable_magasin': responsable_magasin,
               'responsable_magasin_total': responsable_magasin_total, 'datapie': datapie, 'listart': listart, 'listartid': listartid, 'listartnbr': listartnbr, 'datelist': datelist, 'nbrlist': nbrlist}
    return render(request, 'magasin/Responsable/stat.html', context)
