from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, DeleteView
from django.contrib.auth.decorators import login_required
from authentication.decorators import patient_required
from django.utils.decorators import method_decorator
from .models import Patient, Appointment, Disease, Medicine, Test, Suggestion, Exercise, Continue
from hospitals.models import Hospital, MyDoctor, MyDoctorTime, HospitalNews, HospitalService
from doctors.models import Doctor
from authentication.models import User
from .forms import PatientUpdateForm


@method_decorator([login_required, patient_required], name='dispatch')
class PatientDetailView(DetailView):
    template_name = 'patients/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(user=self.request.user)
        return context


@method_decorator([login_required, patient_required], name='dispatch')
class PatientUpdateView(UpdateView):
    template_name = 'patients/update.html'
    model = User
    form_class = PatientUpdateForm

    def get_context_data(self, **kwargs):
        context = super(PatientUpdateView, self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = User.objects.get(id=request.user.id)
            user.first_name = self.request.POST['first_name']
            user.last_name = self.request.POST['last_name']
            user.email = self.request.POST['email']
            user.save()

            patient = Patient.objects.get(user=request.user)

            if 'img' in request.FILES:
                if patient.profile_image:
                    patient.profile_image.delete()
                    patient.profile_image = self.request.FILES['img']
                else:
                    patient.profile_image = self.request.FILES['img']

            patient.address = self.request.POST['address']
            patient.telephone_number = self.request.POST['telephone_number']
            patient.save()
            return redirect("p-profile", slug=user.slug)
        return render(request, self.template_name)


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointmentView(ListView):
    model = Hospital
    context_object_name = 'hospitals'
    template_name = 'patients/appointment.html'

    def get_context_data(self, **kwargs):
        context = super(MakeAppointmentView, self).get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentView(ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'patients/appointment_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user.patient
        ).order_by('status')


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('p-appointment-list')


@method_decorator([login_required, patient_required], name='dispatch')
class DiseaseView(ListView):
    model = Disease
    context_object_name = 'diseases'
    template_name = 'patients/disease_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user.patient
        )


@method_decorator([login_required, patient_required], name='dispatch')
class DiseaseDetailView(DetailView):
    model = Disease
    context_object_name = 'disease'
    template_name = 'patients/disease_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DiseaseDetailView, self).get_context_data(**kwargs)
        context['medicines'] = Medicine.objects.filter(disease=self.object)
        context['tests'] = Test.objects.filter(disease=self.object)
        context['suggestions'] = Suggestion.objects.filter(disease=self.object)
        context['exercises'] = Exercise.objects.filter(disease=self.object)
        context['continues'] = Continue.objects.filter(disease=self.object)
        return context


@method_decorator([login_required, patient_required], name='dispatch')
class HospitalDetailView(DetailView):
    model = Hospital
    context_object_name = 'hospital'
    template_name = 'hospital_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HospitalDetailView, self).get_context_data(**kwargs)
        context['doctors'] = MyDoctor.objects.filter(hospital=self.object)
        context['services'] = HospitalService.objects.filter(
            hospital=self.object)
        context['newses'] = HospitalNews.objects.filter(hospital=self.object)
        return context


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentCheckoutView(View):
    model = Hospital
    template_name = 'patients/appointment_checkout.html'

    def get(self, request, *args, **kwargs):
        hospital = Hospital.objects.get(slug=self.kwargs.get('slug'))
        # doc = Doctor.objects.get(user=self.kwargs.get('pk'))
        doctor = MyDoctor.objects.get(
            my_doctor=self.kwargs.get('pk'), hospital=hospital)
        times = MyDoctorTime.objects.filter(my_doctor=doctor)
        return render(request, self.template_name, {'hospital': hospital, 'doctor': doctor, 'times': times})

    def post(self, request, *args, **kwargs):
        if request.POST:
            patient = Patient.objects.get(user=self.request.POST['patient'])
            hospital = Hospital.objects.get(user=self.request.POST['hospital'])
            doctor = Doctor.objects.get(user=self.request.POST['doctor'])
            my_doctor = MyDoctor.objects.get(
                hospital=hospital, my_doctor=doctor)

            time = MyDoctorTime.objects.get(
                my_doctor=my_doctor, day=self.request.POST['day'])

            appointment = Appointment.objects.create(
                user=patient, hospital=hospital, doctor=doctor, day=time.day, time=time.time_from)
            Disease.objects.create(
                user=patient, hospital=hospital, doctor=doctor, appointment=appointment)
            return redirect('p-appointment-list')

        return redirect('p-appointment-list')
