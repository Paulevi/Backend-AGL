from rest_framework import serializers
from .models import Employee, Schedule, LeaveRequest
from authentification.models import User  # ton User personnalisé


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLES, write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'EMPLOYE')

        # Créer l'utilisateur lié
        user = User.objects.create(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        # Créer l'employé lié
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'employee', 'start_time', 'end_time']


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'start_date', 'end_date', 'approved']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
