from django.db import models
from django.utils import timezone
# Create your models here.



class Categorie(models.Model):
    TYPES = [
        ('alimentaire', 'Produits alimentaires'),
        ('NA', 'Non-alimentaires'),
        ('PMA', 'Produits à marque propre'),
    ]
    idcategorie =  models.fields.AutoField(primary_key=True)
    nomcat = models.CharField(max_length=100)
    types = models.fields.CharField(max_length=100, choices=TYPES)

    def __str__(self):
        return self.nomcat


class Produit(models.Model):
    idproduit = models.fields.AutoField(primary_key=True)
    nomproduit = models.fields.CharField(max_length=100)
    stock = models.fields.IntegerField()
    seuilmin = models.fields.IntegerField()
    categorie = models.ForeignKey('gestionstock.Categorie', on_delete=models.CASCADE, related_name='produits')
    prix = models.fields.IntegerField()

    def __str__(self):
        return f" {self.nomproduit}-{self.prix}"
    

class Fournisseur(models.Model):

    TYPES = [
        ('local', 'Producteur local'),
        ('national', 'Marque nationale'),
        ('international', 'Marque internationale'),
        ('grossiste', 'Grossiste / Centrale d’achat'),
    ]
    idfournisseur = models.fields.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    type_fournisseur = models.CharField(max_length=50, choices=TYPES)
    contact = models.IntegerField()
    adresse = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom
    
class LigneCommande(models.Model):
    commande = models.ForeignKey('gestionstock.Commande', on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('gestionstock.Produit', on_delete=models.CASCADE)
    quantite = models.IntegerField()

    def montant_total(self):
        return self.quantite * self.produit.prix

    def __str__(self):
        return f"{self.produit.nomproduit} x {self.quantite}"
    

class Commande(models.Model):
    idcommande = models.fields.AutoField(primary_key=True)
    fournisseur = models.ForeignKey('gestionstock.Fournisseur', on_delete=models.CASCADE, related_name='commandes')
    datelivraison = models.fields.DateField()

    def __str__(self):
        return f"Commande {self.idcommande}"