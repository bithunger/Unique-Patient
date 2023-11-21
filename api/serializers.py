from rest_framework import serializers
from authentication.models import User
from patients.models import Patient
from hospitals.models import Hospital
from doctors.models import Doctor

        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password',)
        
    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create(username = validated_data['username'])
        if password is not None:
            user.set_password(password)
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
        
        
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
        
        
        
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'