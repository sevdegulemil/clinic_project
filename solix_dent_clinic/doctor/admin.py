from django.contrib import admin
from .models import Doctor, Slot, Appointment, WaitingList


admin.site.register(Doctor)
admin.site.register(Slot)
admin.site.register(Appointment)
admin.site.register(WaitingList)