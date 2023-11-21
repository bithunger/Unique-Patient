from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='api_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration', views.UserRegistrationView.as_view(), name='api_registration'),
    path('user', views.UserApiView.as_view(), name='api_user'),
    path('patient', views.PatientApiView.as_view(), name='api_patient'),
    path('hospital', views.HospitalApiView.as_view(), name='api_hospital'),
    path('doctor', views.DoctorApiView.as_view(), name='api_doctor'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)