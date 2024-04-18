from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BenefitPlans, Employment,EmploymentWorkingTime, JobHistory, Personal

@login_required
def Benefitplans_list(request):
    benefitplans = BenefitPlans.objects.all()
    return render(request, 'hrapp/list_benefitplan.html', {'benefitplans': benefitplans})

@login_required
def Employment_list(request):
    employments = Employment.objects.all()
    return render(request, 'hrapp/list_employment.html', {'employments': employments})

@login_required
def EmploymentWorkingTime_list(request):
    employmentworkingtimes = EmploymentWorkingTime.objects.all()
    return render(request, 'hrapp/list_EmploymentWorkingTime.html', {'employmentworkingtimes': employmentworkingtimes})

@login_required
def Jobhistory_lisst(request):
    jobhistorys = JobHistory.objects.all()
    return render(request, 'hrapp/list_jobhistory.html', {'jobhistorys': jobhistorys})

@login_required
def Personal_list(request):
    personals = Personal.objects.all()
    return render(request, 'hrapp/list_personal.html', {'personals': personals})