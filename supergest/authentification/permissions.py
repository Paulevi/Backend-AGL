from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsGestionnaireStock(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'GESTION_STOCK'


class IsGestionnaireVente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'GESTION_VENTE'


class IsCaissier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CAISSIER'
