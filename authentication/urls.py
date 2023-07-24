from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('registration/hospital/', views.HospitalSignUpView.as_view(), name='registration-hospital'),
    path('registration/patient/', views.PatientSignUpView.as_view(), name='registration-patient'),
    path('registration/doctor/', views.DoctorSignUpView.as_view(), name='registration-doctor'),
    path('send-mail/', views.SendMailView.as_view(), name='send-mail'),
    path('sign-in/', views.SignIn.as_view(), name='sign-in'),
    path('sign-out/', views.SignOut.as_view(), name='sign-out'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)