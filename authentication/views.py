from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login as auth_login, logout
from django.views.generic import CreateView, View
from .forms import RegistrationForm, PatientRegisterForm, HospitalRegisterForm, DoctorRegisterForm
from authentication.models import User, Contact
from patients.models import Patient
from hospitals.models import Hospital
from doctors.models import Doctor
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.mail import send_mail


class RegistrationView(View):
    template_name = 'authentication/register_with.html'

    def get(self, request):
        return render(request, self.template_name)


class PatientSignUpView(CreateView):
    model = User
    form_class = RegistrationForm
    p_form = PatientRegisterForm
    template_name = 'authentication/registration.html'

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password1 = self.request.POST['password1']
            password2 = self.request.POST['password2']
            email = self.request.POST['email']
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('registration-patient')
            elif password1!=password2:
                messages.error(request, "Password didn't match")
                return redirect('registration-patient')
            elif password1==password2 and len(password1)<8:
                messages.error(request, "Password mus be 8 characters")
                return redirect('registration-patient')
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            user.is_patient = True
            user.save()
            
            dob = self.request.POST['dob']
            gender = self.request.POST['gender']    
            telephone_number = self.request.POST['telephone_number']
            Patient.objects.create(user=user, dob=dob, gender=gender, telephone_number=telephone_number)
            auth_login(self.request, user)
            return redirect("home")
        
        return redirect('registration-patient')

    def get(self, request, *args, **kwargs):
        rg_form = self.form_class(**self.get_form_kwargs())
        p_form = self.p_form()
        return render(request, self.template_name, {'rg_form': rg_form, 'p_form': p_form})


class HospitalSignUpView(CreateView):
    model = User
    form_class = RegistrationForm
    p_form = HospitalRegisterForm
    template_name = 'authentication/registration.html'

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password1 = self.request.POST['password1']
            password2 = self.request.POST['password2']
            email = self.request.POST['email']
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('registration-hospital')
            elif password1!=password2:
                messages.error(request, "Password didn't match")
                return redirect('registration-hospital')
            elif password1==password2 and len(password1)<8:
                messages.error(request, "Password mus be 8 characters")
                return redirect('registration-hospital')
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            user.is_hospital = True
            user.save()
            
            hospital_name = self.request.POST['hospital_name']
            establish = self.request.POST['establish']
            telephone_number = self.request.POST['telephone_number']
            address = self.request.POST['address']
            hospital_map = self.request.POST['hospital_map']
            hospital = Hospital.objects.create(user=user, hospital_name=hospital_name, establish=establish,
                                            telephone_number=telephone_number, address=address, hospital_map=hospital_map)
            auth_login(self.request, user)
            return redirect("home")
                
        return redirect('registration-patient')

    def get(self, request, *args, **kwargs):
        rg_form = self.form_class(**self.get_form_kwargs())
        p_form = self.p_form()
        return render(request, self.template_name, {'rg_form': rg_form, 'p_form': p_form})


class DoctorSignUpView(CreateView):
    model = User
    form_class = RegistrationForm
    p_form = DoctorRegisterForm
    template_name = 'authentication/registration.html'

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password1 = self.request.POST['password1']
            password2 = self.request.POST['password2']
            email = self.request.POST['email']
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('registration-doctor')
            elif password1!=password2:
                messages.error(request, "Password didn't match")
                return redirect('registration-doctor')
            elif password1==password2 and len(password1)<8:
                messages.error(request, "Password mus be 8 characters")
                return redirect('registration-doctor')
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
            user.is_doctor = True
            user.save()

            gender = self.request.POST['gender']
            specialty = self.request.POST['specialty']
            qualification = self.request.POST['qualification']
            telephone_number = self.request.POST['telephone_number']
            doctor = Doctor.objects.create(user=user, gender=gender, specialty=specialty,
                                        qualification=qualification, telephone_number=telephone_number)
            auth_login(self.request, user)
            return redirect("home")
        
        return redirect('registration-patient')


    def get(self, request, *args, **kwargs):
        rg_form = self.form_class(**self.get_form_kwargs())
        p_form = self.p_form()
        return render(request, self.template_name, {'rg_form': rg_form, 'p_form': p_form})


class SignIn(View):
    template_name = 'authentication/signin.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.POST:
            username = self.request.POST['username']
            password = self.request.POST['password']
            
            if User.objects.filter(username=username, password=password).exists():
                user = User.objects.get(username=username, password=password)
                auth_login(request, user)
                messages.success(request, 'Sign in Successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Bad Credential!')

        form = self.form_class
        return render(request, self.template_name, {'form': form})


class SignOut(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sign out Successfully!')
        return redirect('sign-in')


class SendMailView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = self.request.POST['name']
            email = self.request.POST['email']
            comment = self.request.POST['comment']

            if name != '':
                Contact.objects.create(
                    name=name,
                    email=email,
                    comment=comment
                )

            subject = 'From Unique-Patient'
            message = f'Name: {name}\nEmail: {email}\n\n\nMessage:- {comment}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['nurhosainlikhon@gmail.com', ]
            send_mail(subject, message, email_from,
                      recipient_list, fail_silently=True)

            messages.success(request, "Your Message was sent successfully")
            return redirect('home')




# if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')

#                 user = authenticate(username=username, password=password)

#                 if user is not None:
#                     auth_login(request, user)
#                     messages.success(request, 'Sign in Successfully!')
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Error')
#             else:
#                 messages.error(request, 'Bad Credential!')