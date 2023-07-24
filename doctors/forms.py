from authentication.models import User
from django import forms
from django.forms import ModelForm


class DoctorUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
