from django.contrib import admin
from gestioncaisse.models import *
# Register your models here.
admin.site.register(Caisse)
admin.site.register(SessionCaisse)
admin.site.register(Vente)
admin.site.register(LigneVente)
