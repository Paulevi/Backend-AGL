from django.contrib import admin
from gestionstock.models import *
# Register your models here.
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(Commande)
admin.site.register(Categorie)
admin.site.register(LigneCommande)