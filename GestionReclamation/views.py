from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from GestionProjet.models import Utilisateur
from GestionReclamation.forms import ReclamationForm, ReclamationUpdate, SolutionForm, SolutionUpdateForm
from GestionReclamation.models import Reclamation, Solution
import datetime
import json
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def search_results(request):
    if request.is_ajax():
        res = None
        reclamation = request.POST.get('reclamation')
        qs = Reclamation.objects.filter(objet__icontains=reclamation)
        if len(qs) > 0 and len(reclamation) > 0:
            data = []
            for pos in qs:
                item = {
                    'id': pos.id,
                    'objet': pos.objet,
                    'description_reclamation': pos.description_reclamation,
                    'utilisateur': pos.utilisateur.id
                }
                data.append(item)
            res = data
        else:
            res = 'Aucune réclamation trouvée...'
        return JsonResponse({'data': res})
    return JsonResponse({})


def search_results_solution(request):
    if request.is_ajax():
        res = None
        solution = request.POST.get('solution')
        qs = Solution.objects.filter(description_solution=solution)
        if len(qs) > 0 and len(solution) > 0:
            data = []
            for pos in qs:
                item = {
                    'id': pos.id,
                    'rec': pos.reclamation_id,
                    'description_solution': pos.description_solution
                }
                data.append(item)
            res = data
        else:
            res = 'Aucune solution trouvée...'
        return JsonResponse({'data': res})
    return JsonResponse({})


def listReclamation(request):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['id']

        cmd = get_object_or_404(Reclamation, id=content)
        solu = Solution.objects.filter(
            reclamation=content, utilisateur=request.session['id'])
        all_solu = solu.count()
        test = False
        if all_solu < 1:
            cmd.delete()
            test = True

        return JsonResponse({"test": test})

    if request.is_ajax():
        idr = request.POST.get('data')
        proj = Reclamation.objects.get(id=idr)
        item = {
            'nom': proj.objet,
            'desc': proj.description_reclamation

        }
        return JsonResponse({"res": item})

    if utilisateur.role == "admin":
        administrateur = utilisateur
        reclamations = administrateur.reclamation_set.all()
        reclamations_envoyee = Reclamation.objects.filter(
            service='IT', statut='en attente')
        reclamations_faire = Reclamation.objects.filter(
            service='IT', statut='prise en charge')
        reclamations_terminer = Reclamation.objects.filter(
            service='IT', statut='terminé')
        context = {'administrateur': administrateur, 'reclamations': reclamations, 'reclamations_envoyee': reclamations_envoyee,
                   'reclamations_faire': reclamations_faire, 'reclamations_terminer': reclamations_terminer}
        return render(request, 'compte/list_reclamation.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        reclamations = responsable.reclamation_set.all()
        reclamations_envoyee = Reclamation.objects.filter(
            service='Projet', statut='en attente')
        reclamations_faire = Reclamation.objects.filter(
            service='Projet', statut='prise en charge')
        reclamations_terminer = Reclamation.objects.filter(
            service='Projet', statut='terminé')
        context = {'responsable': responsable, 'reclamations': reclamations, 'reclamations_envoyee': reclamations_envoyee,
                   'reclamations_faire': reclamations_faire, 'reclamations_terminer': reclamations_terminer}
        return render(request, 'projet/responsable_projet/list_reclamation.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        reclamations = chef_projet.reclamation_set.all()
        reclamations_envoyee = Reclamation.objects.filter(
            service='Projet', statut='en attente')
        reclamations_faire = Reclamation.objects.filter(
            service='Projet', statut='prise en charge')
        reclamations_terminer = Reclamation.objects.filter(
            service='Projet', statut='terminé')
        context = {'chef_projet': chef_projet, 'reclamations': reclamations, 'reclamations_envoyee': reclamations_envoyee,
                   'reclamations_faire': reclamations_faire, 'reclamations_terminer': reclamations_terminer}
        return render(request, 'projet/chef_projet/list_reclamation.html', context)
    else:
        responsable = utilisateur
        reclamations = responsable.reclamation_set.all()
        reclamations_envoyee = Reclamation.objects.filter(
            service='Magasin', statut='en attente')
        reclamations_faire = Reclamation.objects.filter(
            service='Magasin', statut='prise en charge')
        reclamations_terminer = Reclamation.objects.filter(
            service='Magasin', statut='terminé')
        context = {'responsable': responsable, 'reclamations': reclamations, 'reclamations_envoyee': reclamations_envoyee,
                   'reclamations_faire': reclamations_faire, 'reclamations_terminer': reclamations_terminer}
        return render(request, 'magasin/Responsable/list_reclamation.html', context)


def supprimerReclamation(request, reclamations):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=reclamations)
    solutions = reclamations.solution_set.all()
    message = "Voulez-vous supprimer la réclamation ?"
    if request.method == 'POST':
        if solutions.count() > 0:
            message = "Impossible de supprimer une réclamation qui a déjà des solutions !!"
        else:
            reclamations.delete()
            return redirect('listReclamation')
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'item': reclamations, 'administrateur': administrateur,
                   'reclamations': reclamations, 'message': message}
        return render(request, 'compte/supprimer_reclamation.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'item': reclamations, 'responsable': responsable,
                   'reclamations': reclamations, 'message': message}
        return render(request, 'projet/responsable_projet/supprimer_reclamation.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'item': reclamations, 'chef_projet': chef_projet,
                   'reclamations': reclamations, 'message': message}
        return render(request, 'projet/chef_projet/supprimer_reclamation.html', context)
    else:
        responsable = utilisateur
        context = {'item': reclamations, 'responsable': responsable,
                   'reclamations': reclamations, 'message': message}
        return render(request, 'magasin/Responsable/supprimer_reclamation.html', context)


def modifierReclamation(request, reclamations):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=reclamations)
    form = ReclamationUpdate(instance=reclamations)
    if request.method == 'POST':
        form = ReclamationUpdate(request.POST, instance=reclamations)
        if form.is_valid():
            form.save()
            return redirect('listReclamation')
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'form': form, 'administrateur': administrateur,
                   'reclamations': reclamations}
        return render(request, 'compte/modifier_reclamation.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable,
                   'reclamations': reclamations}
        return render(request, 'projet/responsable_projet/modifier_reclamation.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'form': form, 'chef_projet': chef_projet}
        return render(request, 'projet/chef_projet/modifier_reclamation.html', context)
    else:
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable,
                   'reclamations': reclamations}
        return render(request, 'magasin/Responsable/modifier_reclamation.html', context)


def ajouterReclamation(request):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    form = ReclamationForm()
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listReclamation')
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'form': form, 'administrateur': administrateur}
        return render(request, 'compte/ajouter_reclamation.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable}
        return render(request, 'projet/responsable_projet/ajouter_reclamation.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'form': form, 'chef_projet': chef_projet}
        return render(request, 'projet/chef_projet/ajouter_reclamation.html', context)
    else:
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable}
        return render(request, 'magasin/Responsable/ajouter_reclamation.html', context)


def listSolutionReclamation(request, rec):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamation = Reclamation.objects.get(id=rec)
    solutions = reclamation.solution_set.all()
    if solutions.count() == 0:
        reclamation.statut = 'en attente'
        reclamation.save()

    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'administrateur': administrateur,
                   'reclamations': reclamation, 'solutions': solutions}
        return render(request, 'compte/list_solution.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'responsable': responsable,
                   'reclamations': reclamation, 'solutions': solutions}
        return render(request, 'projet/responsable_projet/list_solution.html', context)

    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'chef_projet': chef_projet,
                   'reclamations': reclamation, 'solutions': solutions}
        return render(request, 'projet/chef_projet/list_solution.html', context)
    else:
        responsable = utilisateur
        context = {'responsable': responsable,
                   'reclamations': reclamation, 'solutions': solutions}
        return render(request, 'magasin/Responsable/list_solution.html', context)


def ajouterSolutionReclamation(request, rec):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=rec)
    form = SolutionForm()
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listSolutionReclamation', rec)

    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'form': form, 'administrateur': administrateur,
                   'reclamations': reclamations}
        return render(request, 'compte/ajouter_solution_reclamation.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'responsable': responsable, 'reclamations': reclamations, }
        return render(request, 'projet/responsable_projet/ajouter_solution_reclamation.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'form': form, 'chef_projet': chef_projet,
                   'reclamations': reclamations}
        return render(request, 'projet/chef_projet/ajouter_solution_reclamation.html', context)
    else:
        responsable = utilisateur
        context = {'responsable': responsable, 'reclamations': reclamations,
                   'utilisateur': utilisateur}
        return render(request, 'magasin/Responsable/ajouter_solution_reclamation.html', context)


def modifierSolution(request, rec, sol):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=rec)
    solution = Solution.objects.get(id=sol)
    form = SolutionForm(instance=solution)
    if request.method == 'POST':
        form = SolutionUpdateForm(request.POST, instance=solution)
        if form.is_valid():
            form.save()
            return redirect('listSolutionReclamation', rec)

    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'form': form, 'administrateur': administrateur,
                   'reclamations': reclamations, 'solution': solution}
        return render(request, 'compte/modifier_solution.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable,
                   'reclamations': reclamations, 'solution': solution}
        return render(request, 'projet/responsable_projet/modifier_solution.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'form': form, 'chef_projet': chef_projet,
                   'reclamations': reclamations, 'solution': solution}
        return render(request, 'projet/chef_projet/modifier_solution.html', context)

    else:
        responsable = utilisateur
        context = {'form': form, 'responsable': responsable, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'magasin/Responsable/modifier_solution.html', context)


def supprimerSolution(request, rec, sol):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=rec)
    solution = Solution.objects.get(id=sol)
    if request.method == 'POST':
        solution.delete()
        return redirect('listSolutionReclamation', rec)
    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'item': reclamations, 'administrateur': administrateur, 'solution': solution,
                   'reclamations': reclamations}
        return render(request, 'compte/supprimer_solution.html', context)
    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'item': reclamations, 'responsable': responsable, 'solution': solution,
                   'reclamations': reclamations}
        return render(request, 'projet/responsable_projet/supprimer_solution.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'item': reclamations, 'chef_projet': chef_projet, 'solution': solution,
                   'reclamations': reclamations}
        return render(request, 'projet/chef_projet/supprimer_solution.html', context)

    else:
        responsable = utilisateur
        context = {'responsable': responsable, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'magasin/Responsable/supprimer_solution.html', context)


def detaille(request, rec, sol):
    try:
        if request.session['id']:
            print("SESSION ON")
    except Exception:
        return render(request, 'ErrorAuth.html')
    utilisateur = Utilisateur.objects.get(id=request.session['id'])
    reclamations = Reclamation.objects.get(id=rec)
    solution = Solution.objects.get(id=sol)

    if utilisateur.role == "admin":
        administrateur = utilisateur
        context = {'administrateur': administrateur, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'compte/detaille.html', context)

    elif utilisateur.role == "Responsable":
        responsable = utilisateur
        context = {'responsable': responsable, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'projet/responsable_projet/detaille.html', context)
    elif utilisateur.role == "chefProjet":
        chef_projet = utilisateur
        context = {'chef_projet': chef_projet, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'projet/chef_projet/detaille.html', context)
    else:
        responsable = utilisateur
        context = {'responsable': responsable, 'reclamations': reclamations, 'solution': solution,
                   'utilisateur': utilisateur}
        return render(request, 'magasin/Responsable/detaille.html', context)


def TraitementReclamation(request, rec):
    reclamations = Reclamation.objects.get(id=rec)
    reclamations.statut = 'prise en charge'
    reclamations.save()
    return redirect('listReclamation')


def TreminerReclamation(request, rec):
    reclamations = Reclamation.objects.get(id=rec)
    reclamations.statut = 'terminé'
    reclamations.save()
    return redirect('listReclamation')
