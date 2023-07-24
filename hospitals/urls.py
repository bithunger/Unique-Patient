from django.urls import path,include
from hospitals import views

urlpatterns = [
    # Hospital admin
    path('dashboard/', views.HospitalDashboardView.as_view(), name='dashboard'),
    
    # Hospital profile
    path('<slug:slug>/profile/', views.HospitalDetailView.as_view(), name='profile'),
    path('<slug:slug>/edit-profile/', views.HospitalUpdateView.as_view(), name='hospital-edit-profile'),
    
    # Appointment
    path('appointments/', views.AppointmentView.as_view(), name='appointments'),
    path('make-appointment/', views.MakeAppointmentView.as_view(), name='h-make-appointment'),
    path('<int:pk>/appointment-checkout/', views.AppointmentCheckoutView.as_view(), name='h-appointment-checkout'),
    path('<int:pk>/update-appointment/', views.AppointmentUpdateView.as_view(), name='update-appointment'),
    path('<int:pk>/delete-appointment/', views.AppointmentDeleteView.as_view(), name='delete-appointment'),
    path('<int:pk>/appointment-status/', views.AppointmentStatusView.as_view(), name='appointment-status'),
    
    # Doctor
    path('add-doctor/', views.AddDoctorView.as_view(), name='add-doctor'),
    path('doctor-list/', views.DoctorView.as_view(), name='doctor-list'),
    path('<int:pk>/doctor-detail/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('<slug:slug>/<int:pk>/doctor-update/', views.DoctorUpdateView.as_view(), name='doctor-update'),
    path('<slug:slug>/<slug:day>/appointments/', views.DateWiseAppointmentView.as_view(), name='date-wise-appointments'),
    path('<slug:slug>/ateWise-add-time/', views.DoctorAddTimeView.as_view(), name='doctor-add-time'),
    path('<int:pk>/doctor-delete/', views.DoctorDeleteView.as_view(), name='doctor-delete'),
    
    # Patient
    path('<int:pk>/patient-detail/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patient-list/', views.PatientView.as_view(), name='patient-list'),
    # path('<slug:slug>/patient-update/', views.PatientUpdateView.as_view(), name='patient-update'),
]