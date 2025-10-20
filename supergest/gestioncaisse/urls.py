from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaisseViewSet, SessionCaisseViewSet, VenteViewSet, LigneVenteViewSet

router = DefaultRouter()
router.register(r'caisses', CaisseViewSet)
router.register(r'sessions', SessionCaisseViewSet)
router.register(r'ventes', VenteViewSet)
router.register(r'lignes', LigneVenteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
