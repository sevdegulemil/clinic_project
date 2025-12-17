from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.login_view, name="login_api"),
    path("patient-login/", views.patient_login_page, name="patient_login_page"),
    path("doctor-login/", views.doctor_login_page, name="doctor_login_page"),
    path("patient-signup/", views.patient_signup_page, name="patient_signup_page"),
]
