from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .models import PayRate, Employee

@login_required
def payrate_list(request):
    payrates = PayRate.objects.all()
    return render(request, 'payroll_app/list_payrate__payroll.html', {'payrates': payrates})

@login_required
def employee_list(request):
    Employees = Employee.objects.all()
    total = 0
    for i in Employees:
        total += i.total_payrate()
    content = {'Employees': Employees, 'total':total}
    return render(request, 'payroll_app/list_employee__payroll.html',content)