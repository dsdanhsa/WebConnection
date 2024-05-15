import decimal
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from payroll_app.models import PayRate, Employee
from django.contrib.auth.decorators import login_required
from hrapp.models import BenefitPlans, Employment, EmploymentWorkingTime, JobHistory, Personal
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import base64
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.dateparse import parse_date


def generate_pay_amount_plot(categories, pay_values):
    plt.bar(categories, pay_values)
    plt.xlabel('Employee Number')
    plt.ylabel('Pay Amount')
    plt.title('Pay Amount by Employee Number')

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.getvalue()).decode()
    plt.close()
    return img_base64
@login_required
def totalpayrate(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()

    img_base64 = generate_pay_amount_plot(categories, pay_values)

    content = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'chart_data': img_base64,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess
    }

    return render(request, 'overview_app/home.html', content)

@login_required
def tbtotalpayrate(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()

    img_base64 = generate_pay_amount_plot(categories, pay_values)

    content = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'chart_data': img_base64,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess
    }

    return render(request, 'overview_app/tbtotalpayrate.html', content)

@login_required
def totalvacation(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()

    # Tạo biểu đồ Vacation Days by Employee Number
    plt.bar(categories, vacation_values)
    plt.xlabel('Employee Number')
    plt.ylabel('Vacation Days')
    plt.title('Vacation Days by Employee Number')
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.getvalue()).decode()
    plt.close()

    context = {
        'chart_data': img_base64,
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess' : totalexcess
    }

    return render(request, 'overview_app/tbvacation.html', context)

#tính tổng người sn trong tháng này và list ra
@login_required
def birthday_count(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    current_month = datetime.now().month
    birthdays = Personal.objects.filter(BIRTH_DATE__month=current_month)
    birthday_count = birthdays.count()

    birthday_list = birthdays.values_list('CURRENT_FIRST_NAME', 'CURRENT_MIDDLE_NAME', 'CURRENT_LAST_NAME', 'BIRTH_DATE', 'CURRENT_ADDRESS_1', 'CURRENT_PHONE_NUMBER')

    context = {
        'birthday_count': birthday_count,
        'birthday_list': birthday_list,
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess
    }

    return render(request, 'overview_app/tbbirthday.html',context)

#hàm thông báo về benefit
@login_required
def benefitplan(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    benefits = BenefitPlans.objects.all()
    context = {
        'benefits': benefits,
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess' : totalexcess
    }
    return render(request, 'overview_app/tbbenefitplan.html', context)

#hàm tính tổng ngày ngĩ và liệt kê từng người nghĩ
@login_required
def excessvacationday(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    excess = []
    Employees = Employee.objects.all()
    for employee in Employees:
        if employee.VacationDays > 2:
            excess.append(employee)
    context = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess,
        'excess': excess
    }
    return render(request, 'overview_app/tbexcessvacationday.html', context)

# hàm thông báo ngày kỉ niệm
@login_required
def hiringanniversary(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    employments = Employment.objects.all()
    totalhiring = 0
    hiring_data = []

    current_year = datetime.now().year

    for employment in employments:
        if (current_year - employment.HIRE_DATE_FOR_WORKING.year) >= 3:
            personal = employment.personal
            if personal:
                hiring_data.append({
                    'employment': employment,
                    'personal': personal
                })
                totalhiring += 1

    context = {
        'totalpayrate': totalpayrate,
        'totalvacationday': totalvacationday,
        'birthday_count': birthday_count,
        'totalexcess': totalexcess,
        'hiring_data': hiring_data,
        'totalhiring': totalhiring,
    }
    return render(request, 'overview_app/tbhiringanniversary.html', context)

def hiringngay304(request):
    return render(request, 'overview_app/hiringngay304.html')
def hiringngay75(request):
    return render(request, 'overview_app/hiringngay75.html')
def hiringthanhlapcongty(request):
    return render(request, 'overview_app/hiringthanhlapcongty.html')

#change benefit
@login_required
def changebenefit_detail(request):
    totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess = calculate_totals()
    changebenefits = BenefitPlans.objects.all()
    context = {'changebenefits': changebenefits,
               'totalpayrate': totalpayrate,
               'totalvacationday': totalvacationday,
               'birthday_count': birthday_count,
               'totalexcess': totalexcess,
               }
    return render(request, 'overview_app/tbchangebenefit_detail.html', context)

@login_required
def changebenefit_update(request, benefitid):
    changebenefits = get_object_or_404(BenefitPlans, BENEFIT_PLANS_ID=benefitid)
    if request.method == 'POST':
        planname = request.POST.get('planname')
        deductable = request.POST.get('deductable')
        percentage_copay = request.POST.get('percentage_copay')

        changebenefits.PLAN_NAME = planname
        changebenefits.DEDUCTABLE = deductable
        changebenefits.PERCENTAGE_COPAY = percentage_copay
        changebenefits.save()
        return redirect('benefit_detail')
    return render(request, 'overview_app/changebenefit_update.html', {'changebenefits': changebenefits})


#hàm chung xuất ra các giá trị trong code
def calculate_totals():
    Employees = Employee.objects.all()
    totalpayrate = 0
    totalvacationday = 0
    totalexcess = 0
    categories = []
    pay_values = []
    vacation_values = []

    current_month = datetime.now().month
    birthdays = Personal.objects.filter(BIRTH_DATE__month=current_month)
    birthday_count = birthdays.count()

    for employee in Employees:
        totalpayrate += employee.total_payrate()
        totalvacationday += employee.total_vacationday()
        categories.append(employee.EmployeeNumber)
        pay_values.append(employee.PayRates_idPay.PayAmount)
        vacation_values.append(employee.VacationDays)
        if employee.VacationDays > 2:
            totalexcess += 1
    return totalpayrate, totalvacationday, categories, pay_values, vacation_values, birthday_count, totalexcess

#thay doi thong tin ở HR và Payroll
@login_required
def changeemployee_detail(request):
    employees = Employee.objects.all()
    totalsalary = 0
    totalmember = 0
    for employee in employees:
        totalsalary += employee.total_payrate()
        totalmember += 1
    employments = Employment.objects.all()
    personals = Personal.objects.all()
    employee_data = zip(employees, employments, personals)
    context = {'employee_data':employee_data, 'totalsalary':totalsalary, 'totalmember':totalmember}
    return render(request, 'overview_app/changeemployee_detail.html', context)



#update employee
@login_required
def employee_update(request, employeeid):
    employee = get_object_or_404(Employee, idEmployee=employeeid)

    if request.method == "POST":
        rq_employee_number = request.POST.get("employee_number")
        rq_last_name = request.POST.get("last_name")
        rq_first_name = request.POST.get("first_name")
        rq_ssn = request.POST.get("ssn")
        rq_pay_rate = request.POST.get("pay_rate")
        rq_vacation_days = request.POST.get("vacation_days")
        rq_paid_to_date = request.POST.get("paid_to_date")
        rq_paid_last_year = request.POST.get("paid_last_year")

        employee.EmployeeNumber = rq_employee_number
        employee.LastName = rq_last_name
        employee.FirstName = rq_first_name
        employee.SSN = rq_ssn
        employee.PayRate = rq_pay_rate
        employee.VacationDays = rq_vacation_days
        employee.PaidToDate = rq_paid_to_date
        employee.PaidLastYear = rq_paid_last_year

        employee.save()

        return redirect('overview_app:employee_detail')
    else:
        context = {'employee': employee}
        return render(request, 'overview_app/Update_employee.html', context)

#update employment
@login_required
def employment_update(request, employmentid):
    employment = get_object_or_404(Employment, EMPLOYMENT_ID=employmentid)

    if request.method == "POST":
        try:
            # Parse dates
            hire_date_for_working = parse_date(request.POST.get("hire_date_for_working"))
            termination_date = parse_date(request.POST.get("termination_date"))
            rehire_date_for_working = parse_date(request.POST.get("rehire_date_for_working"))
            last_review_date = parse_date(request.POST.get("last_review_date"))
        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")

        # Update employment object
        employment.EMPLOYMENT_CODE = request.POST.get("employment_code")
        employment.EMPLOYMENT_STATUS = request.POST.get("employment_status")
        employment.HIRE_DATE_FOR_WORKING = hire_date_for_working
        employment.WORKERS_COMP_CODE = request.POST.get("workers_comp_code")
        employment.TERMINATION_DATE = termination_date
        employment.REHIRE_DATE_FOR_WORKING = rehire_date_for_working
        employment.LAST_REVIEW_DATE = last_review_date
        employment.NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH = request.POST.get("number_days_requirement_of_working_per_month")

        employment.save()

        # Redirect to employee_detail page
        return redirect('overview_app:employee_detail')  # Using the correct URL pattern name
    else:
        context = {'employment': employment}
        return render(request, 'overview_app/Update_employment.html', context)

#update personal
@login_required
def personal_update(request, personalid):
    personal = get_object_or_404(Personal, PERSONAL_ID=personalid)

    if request.method == "POST":
        rq_current_first_name = request.POST.get("current_first_name")
        rq_current_last_name = request.POST.get("current_last_name")
        rq_current_middle_name = request.POST.get("current_middle_name")
        rq_birth_date = request.POST.get("birth_date")
        rq_social_security_number = request.POST.get("social_security_number")
        rq_drivers_license = request.POST.get("drivers_license")
        rq_current_address_1 = request.POST.get("current_address_1")
        rq_current_address_2 = request.POST.get("current_address_2")
        rq_current_city = request.POST.get("current_city")
        rq_current_country = request.POST.get("current_country")
        rq_current_zip = request.POST.get("current_zip")
        rq_current_gender = request.POST.get("current_gender")
        rq_current_phone_number = request.POST.get("current_phone_number")
        rq_current_personal_email = request.POST.get("current_personal_email")
        rq_current_marital_status = request.POST.get("current_marital_status")
        rq_ethnicity = request.POST.get("ethnicity")
        rq_shareholder_status = request.POST.get("shareholder_status")
        rq_benefit_plan_id = request.POST.get("benefit_plan")

        # Cập nhật thông tin cá nhân
        personal.CURRENT_FIRST_NAME = rq_current_first_name
        personal.CURRENT_LAST_NAME = rq_current_last_name
        personal.CURRENT_MIDDLE_NAME = rq_current_middle_name
        personal.BIRTH_DATE = rq_birth_date
        personal.SOCIAL_SECURITY_NUMBER = rq_social_security_number
        personal.DRIVERS_LICENSE = rq_drivers_license
        personal.CURRENT_ADDRESS_1 = rq_current_address_1
        personal.CURRENT_ADDRESS_2 = rq_current_address_2
        personal.CURRENT_CITY = rq_current_city
        personal.CURRENT_COUNTRY = rq_current_country
        personal.CURRENT_ZIP = rq_current_zip
        personal.CURRENT_GENDER = rq_current_gender
        personal.CURRENT_PHONE_NUMBER = rq_current_phone_number
        personal.CURRENT_PERSONAL_EMAIL = rq_current_personal_email
        personal.CURRENT_MARITAL_STATUS = rq_current_marital_status
        personal.ETHNICITY = rq_ethnicity
        personal.SHAREHOLDER_STATUS = rq_shareholder_status
        personal.BENEFIT_PLAN = BenefitPlans.objects.get(BENEFIT_PLANS_ID=rq_benefit_plan_id)

        personal.save()

        return redirect('overview_app:employee_detail')
    else:
        benefit_plans = BenefitPlans.objects.all()
        context = {'personal': personal, 'benefit_plans': benefit_plans}
        return render(request, 'overview_app/Update_personal.html', context)

#add emplployee
def employee_add(request):
    if request.method == "POST":
        rq_pay_rate = request.POST.get("pay_rate")
        if rq_pay_rate:
            try:
                rq_pay_rate_decimal = decimal.Decimal(rq_pay_rate)
            except decimal.InvalidOperation:
                raise ValidationError("Pay rate must be a valid decimal number.")
        else:
            rq_pay_rate_decimal = None
        data = Employee(
            EmployeeNumber=request.POST.get("employee_number"),
            LastName=request.POST.get("last_name"),
            FirstName=request.POST.get("first_name"),
            SSN=request.POST.get("ssn"),
            PayRate=rq_pay_rate_decimal,
            PayRates_idPay_id=request.POST.get("PayRates_idPay_id"),
            VacationDays=request.POST.get("vacation_days"),
            PaidToDate=request.POST.get("paid_to_date"),
            PaidLastYear=request.POST.get("paid_last_year")
        )
        data.save()
        return redirect('overview_app:personal_add')
    else:
        context = {'employees': Employee.objects.all(), 'payrate': PayRate.objects.all()}
        return render(request, 'overview_app/Add_employee.html', context)

@login_required
def personal_add(request):
    if request.method == "POST":
        benefit_plan_id = request.POST.get("benefit_plan")
        benefit_plan_instance = BenefitPlans.objects.get(BENEFIT_PLANS_ID=benefit_plan_id)
        datahr2 = Personal(
            PERSONAL_ID= request.POST.get("personalid"),
            CURRENT_FIRST_NAME=request.POST.get("first_name"),
            CURRENT_LAST_NAME=request.POST.get("last_name"),
            CURRENT_MIDDLE_NAME=request.POST.get("middle_name"),
            BIRTH_DATE=request.POST.get("birth_date"),
            SOCIAL_SECURITY_NUMBER=request.POST.get("social_security_number"),
            DRIVERS_LICENSE=request.POST.get("drivers_license"),
            CURRENT_ADDRESS_1=request.POST.get("current_address_1"),
            CURRENT_ADDRESS_2=request.POST.get("current_address_2"),
            CURRENT_CITY=request.POST.get("current_city"),
            CURRENT_COUNTRY=request.POST.get("current_country"),
            CURRENT_ZIP=request.POST.get("current_zip"),
            CURRENT_GENDER=request.POST.get("current_gender"),
            CURRENT_PHONE_NUMBER=request.POST.get("current_phone_number"),
            CURRENT_PERSONAL_EMAIL=request.POST.get("current_personal_email"),
            CURRENT_MARITAL_STATUS=request.POST.get("current_marital_status"),
            ETHNICITY=request.POST.get("ethnicity"),
            SHAREHOLDER_STATUS=request.POST.get("shareholder_status"),
            BENEFIT_PLAN=benefit_plan_instance
        )
        datahr2.full_clean()
        datahr2.save()
        return redirect('overview_app:employment_add')
    else:
        employees = Employee.objects.all()
        benefit_plans = BenefitPlans.objects.all()
        context = {'employees': employees, 'benefit_plans': benefit_plans}
        return render(request, 'overview_app/Add_personal.html', context)

@login_required
def employment_add(request):
    if request.method == "POST":
        try:
            # Tạo employment_id
            num_employments = Employment.objects.count()
            employment_id = num_employments + 1
            personal_id = request.POST.get("personal_id")
            personal = Personal.objects.get(PERSONAL_ID=personal_id)

            employment = Employment(
                EMPLOYMENT_ID=employment_id,
                EMPLOYMENT_CODE=request.POST.get("employment_code"),
                EMPLOYMENT_STATUS=request.POST.get("employment_status"),
                HIRE_DATE_FOR_WORKING=request.POST.get("hire_date_for_working"),
                WORKERS_COMP_CODE=request.POST.get("workers_comp_code"),
                TERMINATION_DATE=request.POST.get("termination_date"),
                REHIRE_DATE_FOR_WORKING=request.POST.get("rehire_date_for_working"),
                LAST_REVIEW_DATE=request.POST.get("last_review_date"),
                NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH=request.POST.get("number_days_requirement_of_working_per_month"),
                personal=personal
            )
            employment.full_clean()
            employment.save()

            return redirect('overview_app:employee_detail')

        except (ValidationError, Personal.DoesNotExist) as e:
            messages.error(request, str(e))
            return redirect('overview_app:employment_add')

    else:
        employees = Employee.objects.all()
        personals = Personal.objects.all()
        context = {'employees': employees, 'personals': personals}
        return render(request, 'overview_app/Add_employment.html', context)

@login_required
def employee_delete(request):
    if request.method == 'GET':
        try:
            employeeid = request.GET['employee_id']
            employmentid = request.GET['employment_id']
            personalid = request.GET['personal_id']

            employee = Employee.objects.get(idEmployee=employeeid)
            employment = Employment.objects.get(EMPLOYMENT_ID=employmentid)
            personal = Personal.objects.get(PERSONAL_ID=personalid)

            employee.delete()
            employment.delete()
            personal.delete()

            context = {'mess': 'Đã xóa thành công'}
            return JsonResponse(context)

        except (Employee.DoesNotExist, Employment.DoesNotExist, Personal.DoesNotExist):
            context = {'mess': 'Không thể xóa. Hồ sơ không tồn tại.'}
            return JsonResponse(context, status=400)

    return JsonResponse({'mess': 'Phương thức không hợp lệ.'}, status=405)
