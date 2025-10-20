from rest_framework import viewsets, status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Caisse, SessionCaisse, Vente, LigneVente
from .serializer import CaisseSerializer, SessionCaisseSerializer, VenteSerializer, LigneVenteSerializer
from authentification.permissions import IsAdmin, IsCaissier, IsGestionnaireVente

class BaseVentePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role in ['ADMIN', 'GESTION_VENTE', 'CAISSIER'])
        )
    
class CaisseViewSet(viewsets.ModelViewSet):
    queryset = Caisse.objects.all()
    serializer_class = CaisseSerializer
    permission_classes = [BaseVentePermission]

class SessionCaisseViewSet(viewsets.ModelViewSet):
    queryset = SessionCaisse.objects.all()
    serializer_class = SessionCaisseSerializer
    permission_classes = [BaseVentePermission]

class VenteViewSet(viewsets.ModelViewSet):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer
    permission_classes = [BaseVentePermission]

class LigneVenteViewSet(viewsets.ModelViewSet):
    queryset = LigneVente.objects.all()
    serializer_class = LigneVenteSerializer
    permission_classes = [BaseVentePermission]

# Create your views here.
