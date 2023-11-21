from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserSerializer, PatientSerializer, DoctorSerializer, HospitalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
    

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = User.objects.get(username = serializer.data['username'])
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'refresh': str(refresh),
                    'access-token': str(refresh.access_token),
                    'payload': serializer.data,
                }
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer()
        return Response(
                {
                    'message': 'This is a protected user view',
                    'status': 200,
                    'payload': serializer.data,
                 
                }
            )
        

class PatientApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PatientSerializer()
        return Response(
                {
                    'message': 'This is a protected Patient view',
                    'status': 200,
                    'payload': serializer.data,
                 
                }
            )
        


class HospitalApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = HospitalSerializer()
        return Response(
                {
                    'message': 'This is a protected Hospital view',
                    'status': 200,
                    'payload': serializer.data,
                }
            )



class DoctorApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = DoctorSerializer()
        return Response(
                {
                    'message': 'This is a protected Doctor view',
                    'status': 200,
                    'payload': serializer.data,
                }
            )

