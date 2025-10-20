from rest_framework import serializers
from .models import Caisse, SessionCaisse, Vente, LigneVente
from gestionstock.models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['idproduit', 'nomproduit', 'prix', 'stock']

class LigneVenteSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True
    )

    class Meta:
        model = LigneVente
        fields = ['id', 'produit', 'produit_id', 'quantite', 'prix_unitaire', 'remise_unitaire', 'prix_apres_remise', 'sous_total']

class VenteSerializer(serializers.ModelSerializer):
    lignes = LigneVenteSerializer(many=True)

    class Meta:
        model = Vente
        fields = [
            'id', 'numero_ticket', 'session_caisse', 'caisse', 'caissier',
            'montant_brut', 'montant_remise', 'montant_tva', 'montant_total',
            'mode_paiement', 'montant_recu', 'monnaie_rendue', 'date_vente', 'statut', 'lignes'
        ]

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')
        vente = Vente.objects.create(**validated_data)

        for ligne_data in lignes_data:
            produit = ligne_data['produit']
            quantite = ligne_data['quantite']
            if produit.stock < quantite:
                raise serializers.ValidationError(f"Stock insuffisant pour {produit.nomproduit}")
            LigneVente.objects.create(vente=vente, **ligne_data)
            produit.stock -= quantite
            produit.save()

        return vente

class CaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caisse
        fields = ['id', 'numero_caisse', 'nom', 'emplacement', 'statut', 'actif']

class SessionCaisseSerializer(serializers.ModelSerializer):
    caisse = CaisseSerializer(read_only=True)
    caisse_id = serializers.PrimaryKeyRelatedField(
        queryset=Caisse.objects.all(), source='caisse', write_only=True
    )

    class Meta:
        model = SessionCaisse
        fields = ['id', 'caisse', 'caisse_id', 'caissier', 'date_ouverture', 'date_fermeture', 'fond_caisse_initial', 'fond_caisse_final', 'montant_ventes', 'nombre_transactions', 'statut']
