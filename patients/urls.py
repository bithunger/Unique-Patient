from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from patients import views

urlpatterns = [
    path('<slug:slug>/profile/', views.PatientDetailView.as_view(), name='p-profile'),
    path('<slug:slug>/update/', views.PatientUpdateView.as_view(), name='p-update'),
    path('make-appointment/', views.MakeAppointmentView.as_view(), name='make-appointment'),
    path('appointment-list/', views.AppointmentView.as_view(), name='p-appointment-list'),
    path('<int:pk>/appointment-list/', views.AppointmentDeleteView.as_view(), name='p-appointment-delete'),
    path('disease-list/', views.DiseaseView.as_view(), name='p-disease-list'),
    path('<int:pk>/disease-detail/', views.DiseaseDetailView.as_view(), name='p-disease-detail'),
    path('<slug:slug>/hospital-detail/', views.HospitalDetailView.as_view(), name='hospital-detail'),
    path('<slug:slug>/appointment-checkout/<int:pk>', views.AppointmentCheckoutView.as_view(), name='appointment-checkout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)