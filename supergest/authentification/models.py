from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('GESTION_STOCK', 'Gestionnaire de stock'),
        ('GESTION_VENTE', 'Gestionnaire des ventes'),
        ('CAISSIER', 'Caissier'),
        ('EMPLOYE', 'Employé'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='EMPLOYE')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
