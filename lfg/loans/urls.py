from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from loans import views

urlpatterns = [
    path(
        'api/loansrequest', views.LoansRequest.as_view(), name='loansrequest'
    ),
    path('api/', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
