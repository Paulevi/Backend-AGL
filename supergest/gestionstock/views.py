from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produit, Fournisseur, Commande
from .serializer import ProduitSerializer, FournisseurSerializer, CommandeSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer


class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produit', 'fournisseur','datelivraison']
