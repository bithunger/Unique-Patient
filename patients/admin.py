from django.contrib import admin
# from .forms import RegistrationForm, UserChangingForm
from .models import Patient, Appointment, Medicine, Suggestion, Test, Disease
from authentication.models import User
# from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     # readonly_fields = ['image']
#     add_form = RegistrationForm
#     form = UserChangingForm
#     model = Patient
#     list_display = ("email", "name", "profile_image", "username", "gender", "dob", "telephone_number", "address", "is_staff", "is_active", "date_joined")
#     list_filter = ("email", "is_staff", "is_active",)
#     fieldsets = (
#         (None, {"fields": ("profile_image", "name", "username", "email", "password", "gender", "dob", "address", "telephone_number")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": (
#                 "profile_image", "email", "username", "password1", "password2", "is_staff",
#                 "is_active", "groups", "user_permissions"
#             )}
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)
    

