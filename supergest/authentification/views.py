from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()  # ou queryset vide
        user = self.request.user
        if user.role == 'ADMIN':
            return self.queryset.all()
        return self.queryset.filter(role='USER')


# Create your views here.
