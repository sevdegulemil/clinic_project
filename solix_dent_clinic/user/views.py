from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient

@login_required
def patient_profile(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)

    if request.method == 'POST':
        # Update User model
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        # Update Patient model
        patient.phone = request.POST.get('phone')
        patient.birth_date = request.POST.get('birth_date')
        patient.gender = request.POST.get('gender')
        patient.blood_type = request.POST.get('blood_type')
        patient.allergies = request.POST.get('allergies')
        patient.save()

        return redirect('user:patient_profile')

    return render(request, 'user/PatientProfilePage.html', {'patient': patient})

@login_required
def patient_home_view(request):
    return render(request, 'user/PatientHomePage.html')
