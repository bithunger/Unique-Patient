from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from doctors import views

urlpatterns = [
    # Profile
    path('<slug:slug>/profile/', views.DoctorDetailView.as_view(), name='d-profile'),
    path('<slug:slug>/update/', views.DoctorUpdateView.as_view(), name='d-update'),
    
    #Appointment
    path('appointments/', views.AppointmentView.as_view(), name='d-appointments'),
    path('<int:pk>/update-appointment/', views.AppointmentUpdateView.as_view(), name='d-update-appointment'),
    path('<int:pk>/add-test/', views.TestAddView.as_view(), name='add-test'),
    path('<int:pk>/add-medicine/', views.MedicineAddView.as_view(), name='add-medicine'),
    path('<int:pk>/add-suggestion/', views.SuggestionAddView.as_view(), name='add-suggestion'),
    path('<int:pk>/add-exercise/', views.ExerciseAddView.as_view(), name='add-exercise'),
    path('<int:pk>/add-continue/', views.ContinueAddView.as_view(), name='add-continue'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)