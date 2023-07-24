from django.db import models
from authentication.models import User
from patient_history import settings
from django import forms
from autoslug import AutoSlugField



class Doctor(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField('Profile image', upload_to='doctors/profiles/', blank=True, null=True)
    gender = models.CharField('Gender', max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField('Date of Birth (YYY-MM-DD)', blank=True, null=True)
    specialty = models.CharField('Specialty', max_length=100, blank=False)
    qualification = models.CharField('Qualification', max_length=150, blank=False)
    address = models.CharField('Address', max_length=300, blank=True)
    telephone_number = models.CharField('Telephone', max_length=20, blank=True)
    status = models.BooleanField('Doctor status',default=True)
  
    def __str__(self):
        return self.user.username


