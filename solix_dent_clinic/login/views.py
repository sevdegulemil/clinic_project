import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from doctor.models import Doctor


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse(
            {"ok": False, "error": "Only POST allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse(
            {"ok": False, "error": "Invalid JSON"},
            status=400
        )

    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return JsonResponse(
            {"ok": False, "error": "Email and password required"},
            status=400
        )

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {"ok": False, "error": "Invalid credentials"},
            status=401
        )

    user = authenticate(
        username=user_obj.username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {"ok": False, "error": "Invalid credentials"},
            status=401
        )

    is_doctor = Doctor.objects.filter(email=user.email).exists()

    return JsonResponse({
        "ok": True,
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": "doctor" if is_doctor else "patient",
    })
