# Generated by Django 5.0.4 on 2024-04-18 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='benefitplans',
            options={'ordering': ['BENEFIT_PLANS_ID']},
        ),
        migrations.AlterModelOptions(
            name='employment',
            options={'ordering': ['EMPLOYMENT_ID']},
        ),
        migrations.AlterModelOptions(
            name='employmentworkingtime',
            options={'ordering': ['EMPLOYMENT_WORKING_TIME_ID']},
        ),
        migrations.AlterModelOptions(
            name='jobhistory',
            options={'ordering': ['JOB_HISTORY_ID']},
        ),
        migrations.AlterModelOptions(
            name='personal',
            options={'ordering': ['PERSONAL_ID']},
        ),
        migrations.AddField(
            model_name='employee',
            name='PaidLastYear',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
