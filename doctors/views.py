from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, DeleteView
from django.contrib.auth.decorators import login_required
from authentication.decorators import doctor_required
from django.utils.decorators import method_decorator
from patients.models import Appointment, Disease, Medicine, Suggestion, Exercise, Continue, Test
from .models import Doctor
from .forms import DoctorUpdateForm
from authentication.models import User


@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorDetailView(DetailView):
    template_name = 'doctors/profile.html'
    model = User
    context_object_name = 'user'


@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorUpdateView(View):
    template_name = 'doctors/update.html'
    model = User
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(slug=self.kwargs.get('slug'))
        return render(request, self.template_name, {'user': user})

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = User.objects.get(id=request.user.id)
            user.first_name = self.request.POST['first_name']
            user.last_name = self.request.POST['last_name']
            user.email = self.request.POST['email']
            user.save()

            doctor = Doctor.objects.get(user=request.user)

            if 'img' in request.FILES:
                if doctor.profile_image:
                    doctor.profile_image.delete()
                    doctor.profile_image = self.request.FILES['img']
                else:
                    doctor.profile_image = self.request.FILES['img']

            doctor.dob = self.request.POST['dob']
            doctor.specialty = self.request.POST['specialty']
            doctor.qualification = self.request.POST['qualification']
            doctor.address = self.request.POST['address']
            doctor.telephone_number = self.request.POST['telephone_number']
            doctor.save()
            return redirect("d-profile", slug=user.slug)
        return render(request, self.template_name)


@method_decorator([login_required, doctor_required], name='dispatch')
class AppointmentView(ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'doctors/appointment_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            doctor=self.request.user.doctor, status=True
        )


@method_decorator([login_required, doctor_required], name='dispatch')
class AppointmentUpdateView(DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'doctors/appointment_update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['disease'] = Disease.objects.get(appointment=self.object)
        context['diseases'] = Disease.objects.filter(
            user=context['disease'].user, appointment=self.object)
        context['medicines'] = Medicine.objects.filter(
            disease=context['disease'])
        context['suggestions'] = Suggestion.objects.filter(
            disease=context['disease'])
        context['exercises'] = Exercise.objects.filter(
            disease=context['disease'])
        context['continues'] = Continue.objects.filter(
            disease=context['disease'])
        context['tests'] = Test.objects.filter(disease=context['disease'])
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            disease.disease_name = self.request.POST['disease_name']
            disease.disease_des = self.request.POST['disease_des']
            disease.save()
        return redirect('d-update-appointment', pk=pk)


@method_decorator([login_required, doctor_required], name='dispatch')
class TestAddView(View):
    model = Test

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            test = self.model.objects.create(
                disease=disease, test_name=self.request.POST['test_name'])
            test.save()
        return redirect('d-update-appointment', pk=pk)


@method_decorator([login_required, doctor_required], name='dispatch')
class MedicineAddView(View):
    model = Medicine

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            medicine_name = self.request.POST['medicine_name']
            times_in_day = self.request.POST['times_in_day']
            continuing_days = self.request.POST['continuing_days']
            medicine = self.model.objects.create(
                disease=disease, medicine_name=medicine_name, times_in_day=times_in_day, continuing_days=continuing_days)
            medicine.save()
            print(medicine)
            print('medicine')
        return redirect('d-update-appointment', pk=pk)


@method_decorator([login_required, doctor_required], name='dispatch')
class SuggestionAddView(View):
    model = Suggestion

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            suggestion = self.model.objects.create(
                disease=disease, suggestion_des=self.request.POST['suggestion_des'])
            suggestion.save()
        return redirect('d-update-appointment', pk=pk)


@method_decorator([login_required, doctor_required], name='dispatch')
class ExerciseAddView(View):
    model = Exercise

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            exercise = self.model.objects.create(
                disease=disease, exercise_des=self.request.POST['exercise_des'])
            exercise.save()
        return redirect('d-update-appointment', pk=pk)


@method_decorator([login_required, doctor_required], name='dispatch')
class ContinueAddView(View):
    model = Continue

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            disease = Disease.objects.get(appointment_id=pk)
            continuing_days = self.request.POST['continuing_days']
            come_after = self.request.POST['come_after']
            continu = self.model.objects.create(
                disease=disease, continuing_days=continuing_days, come_after=come_after)
            continu.save()
        return redirect('d-update-appointment', pk=pk)
