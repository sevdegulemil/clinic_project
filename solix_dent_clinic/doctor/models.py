from django.db import models
from user.models import Patient
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Doctor(models.Model):

    BRANCH_CHOICES = (
        ("GENEL", "Genel Diş"),
        ("COCUK", "Çocuk Diş"),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)

    branch = models.CharField(
        max_length=10,
        choices=BRANCH_CHOICES
    )

    room_number = models.CharField(max_length=5)
    work_start = models.TimeField(default="09:00")
    work_end = models.TimeField(default="15:00")
    base_slot = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.get_branch_display()}"


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default = True)

    class Meta:
        unique_together = ("doctor","start_time")
        ordering = ["start_time"]
    
    def __str__(self):
        return f"{self.doctor} | {self.start_time.strftime('%H:%M')}"




class Appointment(models.Model):
    slot = models.OneToOneField(Slot,on_delete=models.CASCADE,related_name="appointment")

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="appointments")

    status = models.CharField(
        max_length=20,
        choices=[
            ("BOOKED", "Booked"),
            ("CANCELLED", "Cancelled"),
            ("COMPLETED", "Completed"),],
        default="BOOKED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} | {self.slot.start_time.strftime('%Y - %m - %d %H:%M')} | {self.status}"


class WaitingList(models.Model):
    STATUS_CHOICES = (
        ("WAITING", "Waiting"),
        ("NOTIFIED", "Notified"),
        ("EXPIRED", "Expired"),
        ("BOOKED", "Booked"),
    )

    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="waiting_lists"
    )

    slot = models.ForeignKey(
        "Slot",
        on_delete=models.CASCADE,
        related_name="waiting_lists"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="waiting_lists"
    )

    queue_position = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="WAITING"
    )

    notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        if self.status != "NOTIFIED" or not self.notified_at:
            return False
        return timezone.now() > self.notified_at + timedelta(minutes=30)

    def __str__(self):
        return f"{self.patient} | {self.doctor} | sıra: {self.queue_position}"

class IdempotentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
