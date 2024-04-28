from django.urls import path
from .views import totalpayrate, totalvacation, birthday_count, benefitplan, excessvacationday, changebenefit_detail, changebenefit_update

app_name = 'overview_app'

urlpatterns = [
    path('', totalpayrate, name='totalpayrate'),
    path('totalvacation/', totalvacation, name='totalvacation'),
    path('birthday_count/', birthday_count, name='birthday_count'),
    path('benefitplan/', benefitplan, name='benefitplan'),
    path('excess/', excessvacationday, name='excessvacationday'),
    path('benefit_detail/', changebenefit_detail, name='benefit_detail'),
    path('benefit_update/<int:benefitid>/', changebenefit_update, name='benefit_update'),
]
