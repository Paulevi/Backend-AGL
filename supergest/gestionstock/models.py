from django.db import models

# Create your models here.

class Produit(models.Model):
    idproduit = models.fields.AutoField(primary_key=True)
    nomproduit = models.fields.CharField(max_length=100)
    stock = models.fields.IntegerField()
    seuilmin = models.fields.IntegerField()

    def __str__(self):
        return self.nomproduit
    

class Fournisseur(models.Model):
    idfournisseur = models.fields.AutoField(primary_key=True)
    nom = models.fields.CharField(max_length=100)
    prenom = models.fields.CharField(max_length=100)
    contact = models.fields.IntegerField()

    def __str__(self):
        return self.nom
    

class Commande(models.Model):
    idcommande = models.fields.AutoField(primary_key=True)
    quantite = models.fields.IntegerField()
    datelivraison = models.fields.DateField()

    fournisseur = models.ForeignKey('gestionstock.Fournisseur', on_delete=models.CASCADE, related_name='commandes')
    produit = models.ForeignKey('gestionstock.Produit', on_delete=models.CASCADE, related_name='commandes')


    def __str__(self):
        return f"Commande {self.idcommande} - {self.produit.nomproduit}"