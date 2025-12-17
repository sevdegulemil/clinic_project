from django.urls import path
from . import views

app_name = "login"   # 👈 BU SATIR ÇOK ÖNEMLİ

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.login_view, name="login_api"),
    path("patient-login/", views.patient_login_page, name="patient_login_page"),
    path("doctor-login/", views.doctor_login_page, name="doctor_login_page"),
    path("patient-signup/", views.patient_signup_page, name="patient_signup_page"),
    path("patient-home/", views.patient_home_page, name="patient_home_page"),
    path("about/", views.about_page, name="about"),
    path("contact/", views.contact_page, name="contact"),
    path("logout/", views.logout_view, name="logout"),
]
