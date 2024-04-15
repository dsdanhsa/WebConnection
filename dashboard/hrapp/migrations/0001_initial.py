# Generated by Django 5.0.4 on 2024-04-14 13:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BenefitPlans',
            fields=[
                ('BENEFIT_PLANS_ID', models.DecimalField(decimal_places=0, max_digits=18, primary_key=True, serialize=False)),
                ('PLAN_NAME', models.CharField(max_length=10, null=True)),
                ('DEDUCTABLE', models.DecimalField(decimal_places=0, max_digits=18, null=True)),
                ('PERCENTAGE_COPAY', models.DecimalField(decimal_places=0, max_digits=18, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('EMPLOYMENT_ID', models.DecimalField(decimal_places=0, max_digits=18, primary_key=True, serialize=False)),
                ('EMPLOYMENT_CODE', models.CharField(max_length=50, null=True)),
                ('EMPLOYMENT_STATUS', models.CharField(max_length=10, null=True)),
                ('HIRE_DATE_FOR_WORKING', models.DateField(default=django.utils.timezone.now, null=True)),
                ('WORKERS_COMP_CODE', models.CharField(max_length=10, null=True, verbose_name='MÃ CÔNG VIỆC')),
                ('TERMINATION_DATE', models.DateField(null=True)),
                ('REHIRE_DATE_FOR_WORKING', models.DateField(null=True)),
                ('LAST_REVIEW_DATE', models.DateField(null=True)),
                ('NUMBER_DAYS_REQUIREMENT_OF_WORKING_PER_MONTH', models.DecimalField(decimal_places=0, max_digits=18, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentWorkingTime',
            fields=[
                ('EMPLOYMENT_WORKING_TIME_ID', models.DecimalField(decimal_places=0, max_digits=18, primary_key=True, serialize=False)),
                ('YEAR_WORKING', models.DateField(default=django.utils.timezone.now, null=True)),
                ('MONTH_WORKING', models.DecimalField(decimal_places=0, max_digits=2, null=True)),
                ('NUMBER_DAYS_ACTUAL_OF_WORKING_PER_MONTH', models.DecimalField(decimal_places=0, max_digits=2, null=True)),
                ('TOTAL_NUMBER_VACATION_WORKING_DAYS_PER_MONTH', models.DecimalField(decimal_places=0, max_digits=2, null=True)),
                ('EMPLOYMENT', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='working_times', to='hrapp.employment')),
            ],
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('JOB_HISTORY_ID', models.DecimalField(decimal_places=0, max_digits=18, primary_key=True, serialize=False)),
                ('DEPARTMENT', models.CharField(max_length=250, null=True)),
                ('DIVISION', models.CharField(max_length=250, null=True)),
                ('FROM_DATE', models.DateField(default=django.utils.timezone.now, null=True)),
                ('THRU_DATE', models.DateField(null=True)),
                ('JOB_TITLE', models.CharField(max_length=250, null=True)),
                ('SUPERVISOR', models.CharField(max_length=250, null=True)),
                ('LOCATION', models.CharField(max_length=250, null=True)),
                ('TYPE_OF_WORK', models.SmallIntegerField(null=True)),
                ('EMPLOYMENT', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_histories', to='hrapp.employment')),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('PERSONAL_ID', models.DecimalField(decimal_places=0, max_digits=18, primary_key=True, serialize=False)),
                ('CURRENT_FIRST_NAME', models.CharField(max_length=50, null=True)),
                ('CURRENT_LAST_NAME', models.CharField(max_length=50, null=True)),
                ('CURRENT_MIDDLE_NAME', models.CharField(max_length=50, null=True)),
                ('BIRTH_DATE', models.DateField(default=django.utils.timezone.now, null=True)),
                ('SOCIAL_SECURITY_NUMBER', models.CharField(max_length=20, null=True)),
                ('DRIVERS_LICENSE', models.CharField(max_length=50, null=True)),
                ('CURRENT_ADDRESS_1', models.CharField(max_length=255, null=True)),
                ('CURRENT_ADDRESS_2', models.CharField(max_length=255, null=True)),
                ('CURRENT_CITY', models.CharField(max_length=100, null=True)),
                ('CURRENT_COUNTRY', models.CharField(max_length=100, null=True)),
                ('CURRENT_ZIP', models.DecimalField(decimal_places=0, max_digits=18, null=True)),
                ('CURRENT_GENDER', models.CharField(max_length=20, null=True)),
                ('CURRENT_PHONE_NUMBER', models.CharField(max_length=15, null=True)),
                ('CURRENT_PERSONAL_EMAIL', models.CharField(max_length=50, null=True)),
                ('CURRENT_MARITAL_STATUS', models.CharField(max_length=50, null=True)),
                ('ETHNICITY', models.CharField(max_length=10, null=True)),
                ('SHAREHOLDER_STATUS', models.SmallIntegerField(null=True)),
                ('BENEFIT_PLAN', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personals', to='hrapp.benefitplans')),
            ],
        ),
        migrations.AddField(
            model_name='employment',
            name='personal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employments', to='hrapp.personal'),
        ),
    ]
