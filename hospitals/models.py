from django.db import models
from authentication.models import User
# from patients.models import Patient
from doctors.models import Doctor
from autoslug import AutoSlugField

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hospital_image = models.ImageField('Hospital image', upload_to='hospitals/profiles', blank=True, null=True)
    hospital_name = models.CharField('Hospital name', max_length=150, blank=False)
    slug = AutoSlugField(populate_from='hospital_name', unique=True)
    establish = models.DateField('Establish Date (YYY-MM-DD)', blank=False)
    address = models.CharField('Hospital Address', max_length=150, blank=False)
    hospital_about = models.TextField('Hospital about', blank=True)
    telephone_number = models.CharField('Telephone', max_length=20, blank=False)
    hospital_map = models.CharField('Hospital map',max_length=100, blank=False)
    hospital_fb = models.CharField('Hospital FB',max_length=100, blank=True)
    hospital_web = models.CharField('Hospital Web',max_length=100, blank=True)
    status = models.BooleanField('Hospital Status',default=True)
  
    def __str__(self):
        return self.user.username



class MyDoctor(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    my_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    status = models.BooleanField('My doctor status',default=True)
  
    def __str__(self):
        return self.my_doctor.user.username

    
    
class MyDoctorTime(models.Model):
    DAYS = (
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    
    my_doctor = models.ForeignKey(MyDoctor, on_delete=models.CASCADE)
    day = models.CharField('Day', max_length=20, choices=DAYS)
    time_from = models.CharField('Time from', max_length=20, blank=True)
    time_to = models.CharField('Time to', max_length=20, blank=True)
    status = models.BooleanField('Doctor time status',default=True)
    
    def __str__(self):
        return self.day
    
    
    
class HospitalService(models.Model):
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, primary_key=True)
    service_title = models.CharField('My service', max_length=100)
    service_des = models.CharField('My service description', max_length=200)
    slug = AutoSlugField(populate_from='service_title', unique=True)
    status = models.BooleanField('My service status',default=True)
    
    def __str__(self):
        return self.service_title
    
    
    
class HospitalNews(models.Model):
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, primary_key=True)
    news_title = models.CharField('My news', max_length=100)
    news_des = models.CharField('My news description', max_length=200)
    slug = AutoSlugField(populate_from='news_title', unique=True)
    status = models.BooleanField('My news status',default=True)
    
    def __str__(self):
        return self.news_title