from GestionProjet.viewsets import ProjetViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('projet',ProjetViewset)

# localhost:p/api/projet/5
# GET, POST, PUT, DELETE
# list , retrive