from django.db import models
from django.contrib.auth.models import User

# Kliniğimizdeki doktorları temsil eder.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100) # Doktorun uzmanlık alanı, örn: 'Kardiyoloji'

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

# Klinikteki fiziksel odaları temsil eder.
class Room(models.Model):
    name = models.CharField(max_length=50) # Oda adı veya numarası, örn: 'Oda 101'
    capacity = models.IntegerField(default=1) # Odanın aynı anda kaç randevu kaldırabileceği

    def __str__(self):
        return self.name

# Doktorların veya odaların belirli bir tarihteki müsait zaman dilimlerini temsil eder.
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} @ {self.room} ({self.start_time.strftime('%d-%m %H:%M')}) - {'Müsait' if self.is_available else 'Dolu'}"

# Hastaların aldığı randevuları temsil eder.
class Appointment(models.Model):
    # Hasta olarak Django'nun User modelini kullanıyoruz.
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Randevu: {self.patient.username} | {self.timeslot}"

# Uygun bir zaman dilimi için bekleyen hastaları temsil eder.
class WaitingListEntry(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    # Hastanın belirli bir doktor veya sadece bir uzmanlık alanı için bekleyebilmesi
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} bekleme listesinde"
