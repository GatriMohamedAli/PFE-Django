from django.urls import path

from search import views
from search.views import SearchView
app_name='app'
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('<int:id>',views.detail_page,name='detail')

]
