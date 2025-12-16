from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Main calendar view
    path('', views.calendar, name='calendar'),
    
    # API endpoint to get appointment data for the calendar
    path('api/appointments/', views.appointment_data, name='appointment_data'),
    
    # Action to book a timeslot
    path('book/<int:timeslot_id>/', views.book_timeslot, name='book_timeslot'),
    
    # Action to cancel an appointment
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
    # Utility to generate sample data
    path('generate-data/', views.generate_timeslots, name='generate_data'),

    # Waiting List
    path('waitlist/join/', views.add_to_waiting_list, name='join_waitlist'),
]
