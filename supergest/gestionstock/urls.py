from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduitViewSet, FournisseurViewSet, CommandeViewSet

router = DefaultRouter()
router.register(r'produits', ProduitViewSet)
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'commandes', CommandeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
