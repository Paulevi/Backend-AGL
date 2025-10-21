from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from gestionstock.models import Produit, Commande, Fournisseur


class Caisse(models.Model):
    numero_caisse = models.CharField(max_length=10, unique=True,primary_key=True)
    statut = models.CharField(
        max_length=20,
        choices=[('OUVERTE', 'Ouverte'), ('FERMEE', 'Fermée'), ('MAINTENANCE', 'En maintenance')],
        default='FERMEE'
    )
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Caisse {self.numero_caisse}"


class SessionCaisse(models.Model):
    idcaisse = models.IntegerField(primary_key=True)
    caisse = models.ForeignKey(Caisse, on_delete=models.PROTECT, related_name='sessions')
    caissier = models.ForeignKey('authentification.User', on_delete=models.PROTECT, related_name='sessions_caisse')
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(null=True, blank=True)
    fond_caisse_initial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fond_caisse_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_ventes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nombre_transactions = models.IntegerField(default=0)
    ecart_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=[('OUVERTE', 'Ouverte'), ('FERMEE', 'Fermée')], default='OUVERTE')
    commentaires = models.TextField(blank=True)

    def __str__(self):
        return f"Session {self.caisse.numero_caisse} - {self.date_ouverture.date()}"


class Vente(models.Model):
    idvente = models.IntegerField(primary_key=True)
    numero_ticket = models.CharField(max_length=50, unique=True)
    session_caisse = models.ForeignKey(SessionCaisse, on_delete=models.PROTECT, related_name='ventes')
    caisse = models.ForeignKey(Caisse, on_delete=models.PROTECT, related_name='ventes')
    caissier = models.ForeignKey('authentification.User', on_delete=models.PROTECT, related_name='ventes_effectuees')

    montant_brut = models.DecimalField(max_digits=12, decimal_places=2)
    montant_remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=[
        ('ESPECES', 'Espèces'), ('CARTE', 'Carte bancaire'),
        ('MOBILE', 'Mobile Money'), ('CHEQUE', 'Chèque'), ('MIXTE', 'Paiement mixte')
    ])
    montant_recu = models.DecimalField(max_digits=12, decimal_places=2)
    monnaie_rendue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_vente = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[('VALIDEE', 'Validée'), ('ANNULEE', 'Annulée'), ('REMBOURSEE', 'Remboursée')], default='VALIDEE')
    points_fidelite_gagnes = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Calcul monnaie rendue
        if self.montant_recu:
            self.monnaie_rendue = max(0, self.montant_recu - self.montant_total)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.numero_ticket} - {self.montant_total} FCFA"


class LigneVente(models.Model):
    idligne = models.IntegerField(primary_key=True)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, related_name='lignes_vente')
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    remise_unitaire = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    prix_apres_remise = models.DecimalField(max_digits=10, decimal_places=2)
    tva = models.DecimalField(max_digits=5, decimal_places=2)
    sous_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculer le prix après remise
        self.prix_apres_remise = self.prix_unitaire * (1 - self.remise_unitaire / 100)
        # Calculer le sous-total
        self.sous_total = self.quantite * self.prix_apres_remise

        # Mise à jour du stock
        if self.produit.stock < self.quantite:
            raise ValueError(f"Stock insuffisant pour {self.produit.nomproduit}")
        self.produit.stock -= self.quantite
        self.produit.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit.nomproduit} x {self.quantite}"

