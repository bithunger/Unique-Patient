# Generated by Django 4.2.2 on 2023-07-24 10:04

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('doctors', '0001_initial'),
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20, verbose_name='Day')),
                ('time', models.CharField(max_length=20, verbose_name='Time')),
                ('status', models.BooleanField(default=False, verbose_name='Appointment status')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.CharField(blank=True, max_length=100, verbose_name='Disease name')),
                ('disease_des', models.CharField(blank=True, max_length=150, verbose_name='Disease description')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='disease_name', unique=True)),
                ('status', models.BooleanField(default=True, verbose_name='Disease status')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disease_appointment', to='patients.appointment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disease_hospital', to='hospitals.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Eunuch', 'Eunuch')], max_length=20, verbose_name='Gender')),
                ('dob', models.DateField(verbose_name='Date of Birth (YYY-MM-DD)')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='patients/profiles/', verbose_name='Profile image')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Address')),
                ('telephone_number', models.CharField(max_length=20, verbose_name='Telephone')),
                ('status', models.BooleanField(default=True, verbose_name='Patient status')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(blank=True, max_length=100, verbose_name='Test name')),
                ('test_report', models.FileField(blank=True, max_length=150, upload_to='test_reports/', verbose_name='Test report')),
                ('status', models.BooleanField(default=True, verbose_name='Test status')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion_des', models.CharField(blank=True, max_length=150, verbose_name='Suggestion')),
                ('status', models.BooleanField(default=True, verbose_name='Suggestion status')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.disease')),
            ],
        ),
        migrations.CreateModel(
            name='MyPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='My Patient status')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.hospital')),
                ('my_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_patient', to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100, verbose_name='Medicine name')),
                ('times_in_day', models.CharField(max_length=30, verbose_name='Times in a day')),
                ('continuing_days', models.CharField(max_length=30, verbose_name='Continuing days')),
                ('status', models.BooleanField(default=True, verbose_name='Medicine status')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_des', models.CharField(blank=True, max_length=150, verbose_name='Exercise')),
                ('status', models.BooleanField(default=True, verbose_name='Exercise status')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.disease')),
            ],
        ),
        migrations.AddField(
            model_name='disease',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disease_user', to='patients.patient'),
        ),
        migrations.CreateModel(
            name='Continue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continuing_days', models.CharField(blank=True, max_length=50, verbose_name='Continuing days')),
                ('come_after', models.CharField(blank=True, max_length=50, verbose_name='Come again after')),
                ('status', models.BooleanField(default=True, verbose_name='Continue status')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.disease')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient'),
        ),
    ]
