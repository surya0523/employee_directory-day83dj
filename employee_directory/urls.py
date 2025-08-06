# employee_directory/urls.py
from django.contrib import admin
from django.urls import path, include
from employees.views import EmployeeListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', EmployeeListView.as_view(), name='home'),
]