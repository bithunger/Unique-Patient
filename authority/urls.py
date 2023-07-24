from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from authority import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('', views.home, name='home'),
    path('about-us/', views.about, name='about-us'),
    path('services/', views.services, name='services'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)