from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    # Doctor dashboard
    path("", views.doctor_home_page, name="doctor_home"),

    # Appointment cancel (doctor side)
    path(
        "cancel-appointment/<int:appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment"
    ),
    path(
    "confirm-slot/<int:waiting_id>/",
    views.confirm_notified_slot,
    name="confirm_notified_slot"
),
    # API endpoints for patient appointment booking
    path('api/branches/', views.get_branches, name='get_branches'),
    path('api/doctors/', views.get_doctors, name='get_doctors'),
    path('api/slots/', views.get_slots, name='get_slots'),
    path('api/book_appointment/', views.book_appointment, name='book_appointment'),
]
