from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import User
from patients.models import Patient
from hospitals.models import Hospital
from doctors.models import Doctor
from django import forms
from django.forms import ModelForm


class PatientRegisterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = True

    class Meta:
        model = Patient
        fields = ("gender", "dob", "telephone_number")


class HospitalRegisterForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ("hospital_name", "establish",
                  "telephone_number", "address", "hospital_map")
        widgets = {
            'establish': forms.DateInput(attrs={'placeholder': 'YYY-MM-DD'}),
        }


class DoctorRegisterForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ("gender", "specialty", "qualification", "telephone_number")


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "username", 'password1', 'password2')
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control border-bottom', 'id': 'name'}),
        # }


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.PasswordInput()
