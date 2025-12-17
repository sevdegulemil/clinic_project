from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("login.urls")),      # ✅ SADECE BURADA

    path("user/", include("user.urls")),
    path("doctor/", include("doctor.urls")),
]
