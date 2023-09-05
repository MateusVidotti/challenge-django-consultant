from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from loans import views

urlpatterns = [
    path('api/loans', views.Loans.as_view()),
    path('api/loansrequest', views.LoansRequest.as_view()),
    path('api/formsettings', views.FormSettings.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
