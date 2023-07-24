from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from patient_history import settings


def patient_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_patient,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def hospital_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_hospital,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def doctor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_doctor,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
