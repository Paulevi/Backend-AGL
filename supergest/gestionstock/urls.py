from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'commandes', CommandeViewSet)
router.register(r'lignes-commandes', LigneCommandeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
