# employees/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Employee, Department

class HRRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return reverse_lazy('employee_list')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department__id=department_id)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(job_title__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['selected_department'] = self.request.GET.get('department', '')
        context['query'] = self.request.GET.get('q', '')
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Employees', 'url': reverse_lazy('employee_list')},
        ]
        return context

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Employees', 'url': reverse_lazy('employee_list')},
            {'name': employee.full_name(), 'url': employee.get_absolute_url()},
        ]
        return context

class EmployeeCreateView(HRRequiredMixin, CreateView):
    model = Employee
    template_name = 'employees/employee_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'job_title', 'department']
    success_url = reverse_lazy('employee_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Employees', 'url': reverse_lazy('employee_list')},
            {'name': 'Add Employee', 'url': reverse_lazy('employee_add')},
        ]
        return context

class EmployeeUpdateView(HRRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employees/employee_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'job_title', 'department']
    success_url = reverse_lazy('employee_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Employees', 'url': reverse_lazy('employee_list')},
            {'name': employee.full_name(), 'url': employee.get_absolute_url()},
            {'name': 'Edit', 'url': reverse_lazy('employee_edit', kwargs={'pk': employee.pk})},
        ]
        return context

class EmployeeDeleteView(HRRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': reverse_lazy('home')},
            {'name': 'Employees', 'url': reverse_lazy('employee_list')},
            {'name': employee.full_name(), 'url': employee.get_absolute_url()},
            {'name': 'Delete', 'url': reverse_lazy('employee_delete', kwargs={'pk': employee.pk})},
        ]
        return context