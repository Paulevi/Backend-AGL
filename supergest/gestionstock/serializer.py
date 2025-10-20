from rest_framework import serializers
from .models import *

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class ProduitSerializer(serializers.ModelSerializer):
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    besoin_reapprovisionnement = serializers.ReadOnlyField()

    class Meta:
        model = Produit
        fields = '__all__'


class LigneCommandeSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    montant_total = serializers.SerializerMethodField()

    class Meta:
        model = LigneCommande
        fields = '__all__'

    def get_montant_total(self, obj):
        return obj.montant_total()


class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'
