from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
import json


def logout_view(request):
    logout(request)
    return redirect('login:home')


def home(request):
    return render(request, "login/Home.html")

def patient_login_page(request):
    return render(request, "login/PatientSignInPage.html")


def doctor_login_page(request):
    return render(request, "login/DoctorSignInPage.html")


def patient_signup_page(request):
    return render(request, "login/PatientSignUpPage.html")


def patient_home_page(request):
    return render(request, "user/PatientHomePage.html")


def about_page(request):
    return render(request, "login/about.html")


def contact_page(request):
    return render(request, "login/contact.html")



@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"ok": False, "error": "Email and password required"}, status=400)

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)

    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "ok": True,
        "user_id": user.id,
        "email": user.email
    })
