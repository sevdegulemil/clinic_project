from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/', views.patient_profile, name='patient_profile'),
    path('home/', views.patient_home_view, name='patient_home'),
]
