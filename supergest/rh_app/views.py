from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Employee, Schedule, LeaveRequest
from .serializers import (
    EmployeeSerializer, EmployeeCreateSerializer, ScheduleSerializer,
    LeaveRequestSerializer, LoginSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'token_type': 'bearer'
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class CreateEmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "Manager du magasin":
            raise PermissionError("Not authorized")
        serializer.save()


class ScheduleListView(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class CreateScheduleView(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role not in ["Manager du magasin", "Responsable de rayon"]:
            raise PermissionError("Not authorized")
        serializer.save()


class LeaveRequestListView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "Manager du magasin":
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(employee=self.request.user)


class CreateLeaveRequestView(generics.CreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        leave_request = serializer.save(employee=self.request.user)
        if leave_request.employee_id != self.request.user.id and self.request.user.role != "Manager du magasin":
            raise PermissionError("Not authorized")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approve_leave_request(request, request_id):
    if request.user.role != "Manager du magasin":
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    leave_request.approved = True
    leave_request.save()
    return Response({"message": "Leave request approved"})
