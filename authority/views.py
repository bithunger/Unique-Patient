from django.shortcuts import render, HttpResponse
from authentication.models import User
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, View
from django.contrib.auth.decorators import login_required
from authentication.decorators import patient_required, hospital_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        user = User.objects.filter(is_patient=True).count()
        hospital = User.objects.filter(is_hospital=True).count()
        doctor = User.objects.filter(is_doctor=True).count()
        return render(request, 'home.html', {'user': user, 'hospital': hospital, 'doctor': doctor})


def about(request):
    user = User.objects.filter(is_patient=True).count()
    return render(request, 'about.html', {'user': user})


def services(request):
    return render(request, 'services.html')
# Create your views here.
