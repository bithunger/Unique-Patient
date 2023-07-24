from django.contrib import admin
from .models import User
from hospitals.models import Hospital, HospitalService, HospitalNews, MyDoctor, MyDoctorTime
from doctors.models import Doctor
from patients.models import Patient, Appointment, Disease, Medicine, Suggestion, Exercise, Test, Continue

admin.site.register(Patient)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(HospitalNews)
admin.site.register(HospitalService)
admin.site.register(MyDoctor)
admin.site.register(MyDoctorTime)
admin.site.register(Exercise)
admin.site.register(Continue)
admin.site.register(Appointment)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Suggestion)
admin.site.register(Test)
