from django.contrib import admin
from gestionstock.models import Produit,Fournisseur,Commande
# Register your models here.
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(Commande)