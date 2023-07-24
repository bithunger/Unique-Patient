from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username', unique=True)


class Contact(models.Model):
    name = models.CharField('Name', max_length=50)
    email = models.CharField('Email', max_length=50)
    comment = models.CharField('Comment', max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    status = models.BooleanField('Contact status', default=True)
