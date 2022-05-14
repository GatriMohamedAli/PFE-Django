from itertools import chain

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from GestionProjet.models import Projet
from GestionReclamation.models import Reclamation
from Magasin.models import Article


# Create your views here.



class SearchView(ListView):
    template_name = 'search/view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context
    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            projet_results = Projet.objects.search(query)
            article_results = Article.objects.search(query)

            queryset_chain = chain(
                projet_results,
                article_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)
            return qs
            return Projet.objects.search(query=query)
        return Projet.objects.none()
def detail_page(request,id):
    object=get_object_or_404(Projet,pk=id)
    return render(request,'search/detail.html',{'object':object})
