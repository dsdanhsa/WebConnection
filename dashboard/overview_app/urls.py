from django.urls import path
from .views import totalpayrate, totalvacation,birthday_count,benefitplan
app_name = 'overview_app'
urlpatterns = [
    path('', totalpayrate, name='totalpayrate'),
    path('totalvacation/', totalvacation, name='totalvacation'),
    path('birthday_count/', birthday_count, name='birthday_count'),
    path('benefitplan/', benefitplan, name='benefitplan'),
]