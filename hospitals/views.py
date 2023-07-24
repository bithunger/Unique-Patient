from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import patient_required, hospital_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, View, DeleteView
from patients.models import Patient, Appointment, Disease, Medicine, Test, MyPatient
from .models import Hospital, MyDoctor, MyDoctorTime
from authentication.models import User
from doctors.models import Doctor
from patients.forms import PatientUpdateForm
from django.urls import reverse_lazy
import datetime


@method_decorator([login_required, hospital_required], name='dispatch')
class HospitalDetailView(DetailView):
    template_name = 'hospitals/profile.html'
    model = User
    context_object_name = 'hospital'


@method_decorator([login_required, hospital_required], name='dispatch')
class HospitalUpdateView(UpdateView):
    template_name = 'hospitals/profile_edit.html'
    model = User
    form_class = PatientUpdateForm
    context_object_name = 'hospital'

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = User.objects.get(slug=self.kwargs.get('slug'))
            user.first_name = self.request.POST['first_name']
            user.last_name = self.request.POST['last_name']
            user.email = self.request.POST['email']
            user.save()

            hospital = Hospital.objects.get(user=user)

            if 'img' in request.FILES:
                if hospital.hospital_image:
                    hospital.hospital_image.delete()
                    hospital.hospital_image = self.request.FILES['img']
                else:
                    hospital.hospital_image = self.request.FILES['img']

            hospital.hospital_name = self.request.POST['name']
            hospital.telephone_number = self.request.POST['mobile']
            hospital.hospital_about = self.request.POST['about']
            hospital.address = self.request.POST['address']
            hospital.hospital_map = self.request.POST['map']
            hospital.hospital_fb = self.request.POST['fb']
            hospital.hospital_web = self.request.POST['web']
            hospital.save()
            return redirect("profile", slug=user.slug)


@method_decorator([login_required, hospital_required], name='dispatch')
class HospitalDashboardView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'patients': Appointment.objects.filter(hospital=request.user.hospital).values('user_id').distinct().count(),
            'doctors': MyDoctor.objects.filter(hospital=request.user.hospital).values('my_doctor_id').distinct().count()
        }

        # print(datetime.date.today().strftime ("%A"))
        return render(request, 'hospitals/dashboard.html', context)


@method_decorator([login_required, hospital_required], name='dispatch')
class AppointmentView(ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'hospitals/appointment_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            hospital=self.request.user.hospital
        )


@method_decorator([login_required, hospital_required], name='dispatch')
class AppointmentUpdateView(DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'hospitals/appointment_update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['disease'] = Disease.objects.get(appointment=self.object)
        context['tests'] = Test.objects.filter(disease=context['disease'])
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.request.POST:
            if 'test_report' in request.FILES:
                id = self.request.POST['id']
                test = Test.objects.get(id=id)
                if test.test_report:
                    test.test_report.delete()
                    test.test_report = self.request.FILES['test_report']
                else:
                    test.test_report = self.request.FILES['test_report']
                test.save()
        return redirect('update-appointment', pk=pk)


@method_decorator([login_required, hospital_required], name='dispatch')
class AppointmentStatusView(View):
    model = Appointment

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if request.POST:
            appointment = self.model.objects.get(id=pk)
            if 'status' in request.POST:
                appointment.status = True
            else:
                appointment.status = False
            appointment.save()

            if appointment.status == True and appointment.user.my_patient.exists() == False:
                patient = MyPatient.objects.create(
                    hospital=self.request.user.hospital, my_patient=appointment.user)

        return redirect('appointments')


@method_decorator([login_required, hospital_required], name='dispatch')
class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'hospitals/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments')


@method_decorator([login_required, hospital_required], name='dispatch')
class PatientView(ListView):
    model = MyPatient
    context_object_name = 'patients'
    template_name = 'hospitals/patient_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            hospital=self.request.user.hospital
        )


@method_decorator([login_required, hospital_required], name='dispatch')
class PatientDetailView(DetailView):
    model = User
    context_object_name = 'patient'
    template_name = 'hospitals/patient_detail.html'


@method_decorator([login_required, hospital_required], name='dispatch')
class AddDoctorView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'doctors': Doctor.objects.all(),
        }
        return render(request, 'hospitals/add_doctor.html', context)

    def post(self, request, *args, **kwargs):
        if request.POST:
            doctor = self.request.POST['doctor']
            day = self.request.POST['day']
            time_from = self.request.POST['time_from']
            time_to = self.request.POST['time_to']
            doctor = Doctor.objects.get(user_id=doctor)
            my_doctor = MyDoctor.objects.create(
                hospital=self.request.user.hospital, my_doctor=doctor)
            my_doctor_time = MyDoctorTime.objects.create(
                my_doctor=my_doctor, day=day, time_from=time_from, time_to=time_to)
            return redirect("doctor-list")
        return redirect("doctor-list")


@method_decorator([login_required, hospital_required], name='dispatch')
class DoctorView(ListView):
    model = MyDoctor
    context_object_name = 'doctors'
    template_name = 'hospitals/doctor_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            hospital=self.request.user.hospital
        )


@method_decorator([login_required, hospital_required], name='dispatch')
class DoctorDetailView(DetailView):
    model = MyDoctor
    context_object_name = 'doctor'
    template_name = 'hospitals/doctor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailView, self).get_context_data(**kwargs)
        context['times'] = MyDoctorTime.objects.filter(my_doctor=self.object)
        return context


@method_decorator([login_required, hospital_required], name='dispatch')
class DoctorUpdateView(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(slug=self.kwargs.get('slug'))
        doctor = MyDoctor.objects.get(
            hospital=self.request.user.hospital, my_doctor=user.doctor)
        time = MyDoctorTime.objects.get(id=self.kwargs.get('pk'))
        return render(request, 'hospitals/doctor_update.html', {'doctor': doctor, 'time': time})

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = User.objects.get(slug=self.kwargs.get('slug'))
            doctor = MyDoctor.objects.get(
                hospital=self.request.user.hospital, my_doctor=user.doctor)
            my_doctor_time = MyDoctorTime.objects.get(
                my_doctor=doctor, id=self.kwargs.get('pk'))
            my_doctor_time.day = self.request.POST['day']
            my_doctor_time.time_from = self.request.POST['time_from']
            my_doctor_time.time_to = self.request.POST['time_to']
            if 'status' in self.request.POST:
                my_doctor_time.status = True
            else:
                my_doctor_time.status = False
            my_doctor_time.save()

            # my_doctor_time = MyDoctorTime.objects.create(my_doctor=my_doctor, day=day, time_from=time_from, time_to=time_to)
            return redirect("doctor-detail", pk=doctor.id)
        return redirect("doctor-list")


@method_decorator([login_required, hospital_required], name='dispatch')
class DateWiseAppointmentView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(slug=self.kwargs.get('slug'))
        doctor = Doctor.objects.get(user=user.doctor)

        appointments = Appointment.objects.filter(
            hospital=self.request.user.hospital, doctor=doctor, day=self.kwargs.get('day'))
        return render(request, 'hospitals/date_wise_appointment_list.html', {'appointments': appointments})


@method_decorator([login_required, hospital_required], name='dispatch')
class DoctorAddTimeView(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(slug=self.kwargs.get('slug'))
        doctor = MyDoctor.objects.get(
            hospital=self.request.user.hospital, my_doctor=user.doctor)
        return render(request, 'hospitals/doctor_update.html', {'doctor': doctor})

    def post(self, request, *args, **kwargs):
        if request.POST:
            day = self.request.POST['day']
            time_from = self.request.POST['time_from']
            time_to = self.request.POST['time_to']
            user = User.objects.get(slug=self.kwargs.get('slug'))
            doctor = MyDoctor.objects.get(
                hospital=self.request.user.hospital, my_doctor=user.doctor)
            my_doctor_time = MyDoctorTime.objects.create(
                my_doctor=doctor, day=day, time_from=time_from, time_to=time_to)
            return redirect("doctor-detail", pk=doctor.id)
        return redirect("doctor-list")


@method_decorator([login_required, hospital_required], name='dispatch')
class DoctorDeleteView(DeleteView):
    model = MyDoctor
    success_url = reverse_lazy('doctor-list')


@method_decorator([login_required, hospital_required], name='dispatch')
class MakeAppointmentView(ListView):
    model = MyDoctor
    context_object_name = 'doctors'
    template_name = 'hospitals/appointment.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            hospital=self.request.user.hospital
        )


@method_decorator([login_required, hospital_required], name='dispatch')
class AppointmentCheckoutView(View):
    model = Hospital
    template_name = 'hospitals/appointment_checkout.html'

    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        doctor = MyDoctor.objects.get(my_doctor=self.kwargs.get(
            'pk'), hospital=request.user.hospital)
        times = MyDoctorTime.objects.filter(my_doctor=doctor)
        return render(request, self.template_name, {'patients': patients, 'doctor': doctor, 'times': times})

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
            return redirect('appointments')

        return redirect('appointments')
