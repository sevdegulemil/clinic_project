from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="patient")
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other"),]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    BLOOD_TYPE_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)

    allergies = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
