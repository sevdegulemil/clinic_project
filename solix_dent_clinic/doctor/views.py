from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Doctor, Slot, Appointment, WaitingList
from user.models import Patient
from django.db.models import Max
from django.utils import timezone
from datetime import datetime
import json
from django.http import JsonResponse
from datetime import datetime
from .models import Slot, Appointment
from user.models import Patient

def available_slots(request):
    doctor_id = request.GET.get("doctor_id")
    date_str = request.GET.get("date") 
    if not doctor_id or not date_str:
        return JsonResponse({"slots": []})

    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    slots = Slot.objects.filter(
        doctor_id=doctor_id,
        start_time__date=date,
        is_active=True
    )

    booked_slots = Appointment.objects.filter(
        slot__in=slots,
        status="BOOKED"
    ).values_list("slot_id", flat=True)

    available = slots.exclude(id__in=booked_slots)

    data = []
    for s in available:
        data.append({
            "id": s.id,
            "start": s.start_time.strftime("%H:%M"),
            "end": s.end_time.strftime("%H:%M"),
        })

    return JsonResponse({"slots": data})

@login_required
def doctor_home_page(request):

    try:
        doctor = Doctor.objects.get(email=request.user.email)
    except Doctor.DoesNotExist:
        return render(
            request,
            "error_page.html",
            {"message": "You are not authorized to view this page."}
        )

    today = timezone.now().date()

    appointments = Appointment.objects.filter(
        slot__doctor=doctor,
        slot__start_time__date=today,
        status="BOOKED"
    ).select_related(
        "slot",
        "patient",
        "patient__user"
    ).order_by("slot__start_time")

    booked_slot_ids = appointments.values_list("slot__id", flat=True)

    available_slots = Slot.objects.filter(
        doctor=doctor,
        start_time__date=today,
        is_active=True
    ).exclude(
        id__in=booked_slot_ids
    ).order_by("start_time")

    calendar_events = []

    for app in appointments:
        calendar_events.append({
            "id": f"app_{app.id}",
            "title": f"{app.patient.user.first_name} {app.patient.user.last_name}",
            "start": app.slot.start_time.isoformat(),
            "end": app.slot.end_time.isoformat(),
            "color": "#3b5173",
            "type": "appointment",
        })

    for slot in available_slots:
        calendar_events.append({
            "id": f"slot_{slot.id}",
            "title": "Müsait",
            "start": slot.start_time.isoformat(),
            "end": slot.end_time.isoformat(),
            "display": "background",
            "color": "#d1e7dd",
            "type": "available_slot",
        })

    waiting_list_entries = WaitingList.objects.filter(
        doctor=doctor,
        slot__start_time__date=today,
        status__in=["WAITING", "NOTIFIED"]
    ).select_related(
        "patient",
        "patient__user"
    ).order_by("queue_position")

    total_slots_today = Slot.objects.filter(
        doctor=doctor,
        start_time__date=today
    ).count()

    booked_slots_today = appointments.count()

    occupancy_percentage = 0
    if total_slots_today > 0:
        occupancy_percentage = (booked_slots_today / total_slots_today) * 100

    context = {
        "doctor": doctor,
        "calendar_events_json": json.dumps(calendar_events),
        "waiting_list_entries": waiting_list_entries,
        "occupancy_percentage": round(occupancy_percentage),
        "booked_slots_count": booked_slots_today,
        "free_slots_count": total_slots_today - booked_slots_today,
        "today_date": today.strftime("%d %b"),
    }

    return render(request, "doctor/DoctorHomePage.html", context)


def handle_slot_freed(slot):
    # Bu slot için sırada bekleyen var mı?
    waiting = WaitingList.objects.filter(
        slot=slot,
        status="WAITING"
    ).order_by("queue_position").first()

    if not waiting:
        # Kimse yoksa slot tekrar aktif
        slot.is_active = True
        slot.save()
        return

    # İlk kişiye 30 dk hak ver
    waiting.status = "NOTIFIED"
    waiting.notified_at = timezone.now()
    waiting.save()

    # Şimdilik sadece log (ileride notification olacak)
    print(
        f"[WAITING LIST] "
        f"{waiting.patient.user.email} için slot açıldı (30 dk süresi var)"
    )


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    # Sadece ilgili doktor iptal edebilir
    if appointment.slot.doctor.email != request.user.email:
        return JsonResponse(
            {"error": "Yetkisiz işlem"},
            status=403
        )

    # Randevuyu iptal et
    appointment.status = "CANCELLED"
    appointment.save()

    slot = appointment.slot

    # Slot boşa çıktı → waiting list kontrol et
    handle_slot_freed(slot)

    return JsonResponse({
        "status": "cancelled",
        "message": "Randevu iptal edildi"
    })

@login_required
def confirm_notified_slot(request, waiting_id):
    waiting = get_object_or_404(WaitingList, id=waiting_id)

    # Sadece ilgili hasta alabilir
    if waiting.patient.user != request.user:
        return JsonResponse(
            {"error": "Bu slot size ait değil"},
            status=403
        )

    # Süre dolmuş mu?
    if waiting.status != "NOTIFIED":
        return JsonResponse(
            {"error": "Bu slot artık geçerli değil"},
            status=400
        )

    # Aynı gün aynı doktora başka randevu var mı?
    already_booked = Appointment.objects.filter(
        patient=waiting.patient,
        slot__doctor=waiting.doctor,
        slot__start_time__date=waiting.slot.start_time.date(),
        status="BOOKED"
    ).exists()

    if already_booked:
        return JsonResponse(
            {"error": "Aynı gün zaten randevunuz var"},
            status=400
        )

    # RANDEVU OLUŞTUR
    Appointment.objects.create(
        slot=waiting.slot,
        patient=waiting.patient,
        status="BOOKED"
    )

    # Waiting list durumunu güncelle
    waiting.status = "BOOKED"
    waiting.save()

    # Aynı slot için bekleyen diğerlerini sil
    WaitingList.objects.filter(
        slot=waiting.slot
    ).exclude(
        id=waiting.id
    ).delete()

    # Slot artık dolu
    waiting.slot.is_active = False
    waiting.slot.save()

    return JsonResponse({
        "status": "success",
        "message": "Randevu başarıyla alındı"
    })



def add_patient_to_waiting_list(patient, slot):
    doctor = slot.doctor
    slot_date = slot.start_time.date()

    already_waiting = WaitingList.objects.filter(
        doctor=doctor,
        patient=patient,
        slot__start_time__date=slot_date,
        status__in=["WAITING", "NOTIFIED"]
    ).exists()

    if already_waiting:
        return False

    last_position = WaitingList.objects.filter(
        doctor=doctor,
        slot=slot
    ).aggregate(
        Max("queue_position")
    )["queue_position__max"]

    if last_position is None:
        last_position = 0

    WaitingList.objects.create(
        doctor=doctor,
        slot=slot,
        patient=patient,
        queue_position=last_position + 1,
        status="WAITING"
    )

    return True

@login_required
def get_branches(request):
    branches = Doctor.objects.values_list('branch', flat=True).distinct()
    print("Branches found:", list(branches))
    return JsonResponse(list(branches), safe=False)

@login_required
def get_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Get all active slots for the doctor on the given date
    all_slots = Slot.objects.filter(
        doctor_id=doctor_id, 
        start_time__date=date, 
        is_active=True
    )
    
    # Get all booked appointments for the doctor on the given date
    booked_appointments = Appointment.objects.filter(
        slot__doctor_id=doctor_id,
        slot__start_time__date=date,
        status="BOOKED"
    ).values_list('slot_id', flat=True)
    
    # Exclude booked slots
    available_slots = all_slots.exclude(id__in=booked_appointments)
    
    slots_data = [
        {
            "id": slot.id,
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
        } 
        for slot in available_slots
    ]
    
    return JsonResponse(slots_data, safe=False)

@login_required
def book_appointment(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        patient = request.user.patient
        
        # Check if the slot is already booked
        if Appointment.objects.filter(slot_id=slot_id, status="BOOKED").exists():
            return JsonResponse({'status': 'error', 'message': 'This slot is already booked.'}, status=400)

        # Check if patient already has an appointment on the same day
        slot = get_object_or_404(Slot, id=slot_id)
        if Appointment.objects.filter(patient=patient, slot__start_time__date=slot.start_time.date(), status="BOOKED").exists():
            return JsonResponse({'status': 'error', 'message': 'You can only book one appointment per day.'}, status=400)
            
        appointment = Appointment.objects.create(slot_id=slot_id, patient=patient, status="BOOKED")
        
        # Deactivate the slot
        slot.is_active = False
        slot.save()
        
        return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
def get_doctors(request):
    branch = request.GET.get("branch")

    doctors = Doctor.objects.filter(branch=branch)

    data = [
        {
            "id": d.id,
            "name": f"{d.first_name} {d.last_name}"
        }
        for d in doctors
    ]

    return JsonResponse(data, safe=False)