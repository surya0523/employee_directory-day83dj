# employees/urls.py
from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView
)

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employee/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]