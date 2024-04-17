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
    totalpayrate = 0
    totalvacationday = 0
    for i in Employees:
        totalpayrate += i.total_payrate()
    for i in Employees:
        totalvacationday += i.total_vacationday()
    content = {'Employees': Employees, 'totalpayrate':totalpayrate, 'totalvacationday': totalvacationday}
    return render(request, 'payroll_app/list_employee__payroll.html',content)


