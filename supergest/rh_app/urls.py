from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/create/', views.CreateEmployeeView.as_view(), name='create-employee'),
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', views.CreateScheduleView.as_view(), name='create-schedule'),
    path('leave-requests/', views.LeaveRequestListView.as_view(), name='leave-request-list'),
    path('leave-requests/create/', views.CreateLeaveRequestView.as_view(), name='create-leave-request'),
    path('leave-requests/<int:request_id>/approve/', views.approve_leave_request, name='approve-leave-request'),
]