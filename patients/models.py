from django.db import models
from authentication.models import User
from hospitals.models import Hospital
from doctors.models import Doctor
from patient_history import settings
from django import forms
from autoslug import AutoSlugField


class Patient(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Eunuch', 'Eunuch'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField('Gender', max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField('Date of Birth (YYY-MM-DD)')
    profile_image = models.ImageField('Profile image', upload_to='patients/profiles/', blank=True, null=True)
    address = models.CharField('Address', max_length=200, blank=True)
    telephone_number = models.CharField('Telephone', max_length=20)
    status = models.BooleanField('Patient status',default=True)
  
    def __str__(self):
        return self.user.username
    


class Appointment(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField('Day', max_length=20)
    time = models.CharField('Time', max_length=20)
    status = models.BooleanField('Appointment status',default=False)
  
    def __str__(self):
        return self.user.user.username
    
    def get_hospital(self):
        return self.hospital.hospital_name
    
    
    
class Disease(models.Model):
    user = models.ForeignKey(Patient, related_name='disease_user', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, related_name='disease_hospital', on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, related_name='disease_appointment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    disease_name = models.CharField('Disease name', max_length=100, blank=True)
    disease_des = models.CharField('Disease description', max_length=150, blank=True)
    slug = AutoSlugField(populate_from='disease_name', unique=True)
    status = models.BooleanField('Disease status',default=True)
  
    def __str__(self):
        return self.disease_name



class Medicine(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    medicine_name = models.CharField('Medicine name', max_length=100)
    times_in_day = models.CharField('Times in a day', max_length=30)
    continuing_days = models.CharField('Continuing days', max_length=30)
    status = models.BooleanField('Medicine status',default=True)
  
    def __str__(self):
        return self.medicine_name
    

class Suggestion(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    suggestion_des = models.CharField('Suggestion', max_length=150, blank=True)
    status = models.BooleanField('Suggestion status',default=True)
  
    def __str__(self):
        return self.suggestion_des
    
    
    
class Continue(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    continuing_days = models.CharField('Continuing days', max_length=50, blank=True)
    come_after = models.CharField('Come again after', max_length=50, blank=True)
    status = models.BooleanField('Continue status',default=True)
  
    def __str__(self):
        return self.continuing_days

    

class Exercise(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    exercise_des = models.CharField('Exercise', max_length=150, blank=True)
    status = models.BooleanField('Exercise status',default=True)
  
    def __str__(self):
        return self.exercise_des

    

class Test(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    test_name = models.CharField('Test name', max_length=100, blank=True)
    test_report = models.FileField('Test report', upload_to='test_reports/', max_length=150, blank=True)
    status = models.BooleanField('Test status',default=True)
  
    def __str__(self):
        return self.test_name
    
    
    
class MyPatient(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    my_patient = models.ForeignKey(Patient, related_name='my_patient', on_delete=models.CASCADE)
    
    status = models.BooleanField('My Patient status',default=True)
  
    def __str__(self):
        return self.my_patient.user.username

