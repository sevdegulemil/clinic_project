import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Doctor, Room, TimeSlot, Appointment, WaitingListEntry

# --- User Authentication ---

def register(request):
    """ Handles user registration. """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in
            return redirect('calendar')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- Main Calendar Views ---

def calendar(request):
    """ Renders the main calendar view. """
    doctors = Doctor.objects.all()
    rooms = Room.objects.all()
    context = {'doctors': doctors, 'rooms': rooms}
    return render(request, 'calendar.html', context)

def appointment_data(request):
    """ API endpoint to fetch timeslot data for the calendar. """
    timeslots = TimeSlot.objects.all().select_related('doctor__user', 'room')
    
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        timeslots = timeslots.filter(doctor_id=doctor_id)
        
    room_id = request.GET.get('room_id')
    if room_id:
        timeslots = timeslots.filter(room_id=room_id)

    events = []
    for ts in timeslots:
        events.append({
            'id': ts.id,
            'title': f"Dr. {ts.doctor.user.first_name} - {ts.room.name}",
            'start': ts.start_time.isoformat(),
            'end': ts.end_time.isoformat(),
            'color': 'green' if ts.is_available else 'red',
            'is_available': ts.is_available
        })
    return JsonResponse(events, safe=False)

# --- Appointment Actions ---

@login_required
@transaction.atomic
def book_timeslot(request, timeslot_id):
    """
    Handles booking a timeslot.
    HACKATHON-NOTE on Locking:
    - Primary lock should be Redis. `select_for_update()` is the DB fallback.
    """
    try:
        # Fallback DB lock:
        timeslot = TimeSlot.objects.select_for_update().get(id=timeslot_id)
        if not timeslot.is_available:
            return JsonResponse({'status': 'error', 'message': 'This timeslot is no longer available.'}, status=409)

        timeslot.is_available = False
        timeslot.save()
        Appointment.objects.create(patient=request.user, timeslot=timeslot)
        return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully.'})
    except TimeSlot.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Timeslot not found.'}, status=404)

@login_required
def cancel_appointment(request, appointment_id):
    """ Handles cancelling an appointment. """
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    timeslot = appointment.timeslot
    timeslot.is_available = True
    timeslot.save()
    
    appointment.delete()
    
    handle_cancelled_appointment(appointment) # Trigger waiting list logic
    
    return redirect('calendar')

# --- Advanced Feature Placeholders ---

def priority_engine_suggest_slot(patient):
    """ HACKATHON-PLACEHOLDER: Suggests the best available slot. """
    return TimeSlot.objects.filter(is_available=True).order_by('start_time').first()

@login_required
def add_to_waiting_list(request):
    """ HACKATHON-PLACEHOLDER: Adds the current user to the waiting list. """
    WaitingListEntry.objects.get_or_create(patient=request.user)
    return redirect('calendar')

def handle_cancelled_appointment(appointment):
    """ HACKATHON-PLACEHOLDER: Handles waiting list logic on cancellation. """
    print(f"Slot {appointment.timeslot.id} is now free. Checking waiting list...")
    next_in_line = WaitingListEntry.objects.order_by('created_at').first()
    if next_in_line:
        print(f"Notifying {next_in_line.patient.username} about the open slot.")
        # NOTIFICATION_LOGIC_HERE()
        next_in_line.delete()

# --- Utility ---

def generate_timeslots(request):
    """ Utility to generate sample data for demonstration. """
    Appointment.objects.all().delete()
    TimeSlot.objects.all().delete()
    Doctor.objects.all().delete()
    Room.objects.all().delete()
    User.objects.filter(is_superuser=False, is_staff=False).delete()

    user1, _ = User.objects.get_or_create(username='drevans', defaults={'first_name':'John', 'last_name':'Evans'})
    doc1, _ = Doctor.objects.get_or_create(user=user1, defaults={'specialty':'Cardiology'})
    
    user2, _ = User.objects.get_or_create(username='drsalih', defaults={'first_name':'Ayşe', 'last_name':'Salih'})
    doc2, _ = Doctor.objects.get_or_create(user=user2, defaults={'specialty':'Neurology'})

    room1, _ = Room.objects.get_or_create(name='Room 101')
    room2, _ = Room.objects.get_or_create(name='Room 102')

    today = datetime.date.today()
    for day in range(5):
        current_date = today + datetime.timedelta(days=day)
        for hour in range(9, 17):
            doctor, room = (doc1, room1) if hour % 2 == 0 else (doc2, room2)
            TimeSlot.objects.create(
                doctor=doctor,
                room=room,
                start_time=datetime.datetime(current_date.year, current_date.month, current_date.day, hour, 0, 0),
                end_time=datetime.datetime(current_date.year, current_date.month, current_date.day, hour, 50, 0),
                is_available=True
            )
    return JsonResponse({'status': 'success', 'message': 'Sample data generated successfully.'})