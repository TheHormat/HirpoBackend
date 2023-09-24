from rest_framework import generics
from rest_framework.response import Response
from .serializers import EmployeeSerializer,RegistrationSerializer, VerifySerializer, SendResetCodeSerializer,ChangePasswordSerializer,ActivationSerializer,EmployeeChangePassword
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.utils import *
from account.models import *
from rest_framework.views import APIView
from account.api.permissions import IsCompanyLead,HasEmployeeOrNot
User = get_user_model()

class LoginView(APIView):
    # permission_classes = [IsCompanyLead]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"sifre ve ya username yanlisdir"})
        login(request, user)
        
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
            
        }
        return Response({"username": username, "tokens": tokens,"userId":user.id}, status=201)


class RegistrationView(APIView):     
    def post(self,request,format=None):
        print(request.data)
        data = request.data
        first_name = data.pop('firstName')
        last_name = data.pop('lastName')
        user_serializer = RegistrationSerializer(data=data)
        
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()
     
        employeeSerializer = EmployeeSerializer(data={"first_name":first_name,"last_name":last_name,"user":user.id,"is_systemadmin":True})
        employeeSerializer.is_valid(raise_exception=True)
        
        employee = employeeSerializer.save()

        return Response({"Status": "success", "data": user_serializer.data}, status=200)




class VerifyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = VerifySerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj=self.get_object()
        serializer = self.serializer_class(data=request.data,instance=obj)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = Activationcode.objects.get(user=user)
        code.delete()

        return Response({"Status": "success"}, status=201)
    
    
class SendResetCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = User.objects.get(email=serializer.data['email']).id
        activation_code_serializer = ActivationSerializer(data={"user":id})
        activation_code_serializer.is_valid(raise_exception=True)
        activation_code_serializer.save()
        print(activation_code_serializer,'actikseria')
        return Response({"id":id,"data": serializer.data,"Status":"success"},status=201)
    

    
class ChangePasswordVerifyView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data,instance=obj)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        code = Activationcode.objects.get(user=user)
        code.delete()
        return Response({'Status':'Success'}, status=201)

class EmployeeChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = EmployeeChangePassword
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        print(request.data)
        serializer = self.serializer_class(data=request.data,instance=obj)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message':'Success'}, status=201)