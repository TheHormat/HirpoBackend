from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from account.utils import create_activation_code,create_password_reset_code
from account.models import *
from wizard.models import Employee
User = get_user_model()




class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type":"password"})
    matchPassword = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model = User
        fields = ("email","password","username", "id","matchPassword")
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "slug": {
                "read_only": True
            }
        }


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        matchPassword = attrs.pop("matchPassword")
        username = attrs.get("username")
        username_qs = User.objects.filter(username=username).exists()
        email_qs = User.objects.filter(email=email).exists()
        if password != matchPassword:
            raise serializers.ValidationError("Password tekrarinda xeta bas verib")
        if email_qs:
            raise serializers.ValidationError("Bu email ile artiq qeydiyyatdan kecilib")
        if username_qs:
            raise serializers.ValidationError("Bu username ile artiq qeydiyyatdan kecilib")
        if password:
            if len(password) < 6:
                raise serializers.ValidationError("Sifre en azi 6 simvoldan ibaret olmalidir")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(
            **validated_data
        )
        user.set_password(password)
        
        user.is_active = True
        user.save()   

        # send mail
    
        return user



class VerifySerializer(serializers.ModelSerializer):
    activation_code=serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ("activation_code",)
        extra_kwargs = {
            "activation_code": {
                "write_only": True
            }
        }
        
    def validate(self, attrs):
        activation_code = Activationcode.objects.get(user=User.objects.get(username=self.instance)).activation_code
        print(activation_code)
        code=attrs.get("activation_code")
        if int(code) != int(activation_code):
            raise serializers.ValidationError({"Duzgun kod daxil edilmeyib"})
        
        return attrs

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()
        return instance
    
    
class SendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        user = User(**attrs)
        email_qs = User.objects.filter(email=email).exists()

        
        
        if not email_qs:
            return {"error":"Bu email ile hesab movcud deyil"}
        
        
        return attrs
    
   

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type":"password"})

    password_reset_code = serializers.CharField()
    class Meta:
        model = User
        fields = ("password_reset_code", "password")
    def validate(self, attrs):
        
        
        code = Activationcode.objects.get(user=User.objects.get(username=self.instance)).activation_code
        password_reset_code = attrs.get("password_reset_code")

        if int(code) != int(password_reset_code):
            raise serializers.ValidationError({"Duzgun kod daxil edilmeyib"})
       
        return attrs

    def update(self,instance,validated_data):
        password = validated_data.pop('password')
        instance.password_reset_code = None
        instance.set_password(password)
        instance.save()
        return instance
        
class ActivationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activationcode
        fields = '__all__' 
        
    def create(self, validated_data):
        
        Code = Activationcode(
            **validated_data
        )
        Code.activation_code = create_activation_code(size=10, model_=Activationcode)
        Code.save()
        
        send_mail(
            'Qeydiyyat tamamla',
            f'Asagidaki koddan istifade ederek qeydiyyati tamamlayin \n Kod: {Code.activation_code}',
            settings.EMAIL_HOST_USER,
            [Code.user.email],
            fail_silently=False,
        )
        return Code
    
class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ("user", "is_systemadmin","first_name","last_name")
        
        
class EmployeeChangePassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password")
    
    def update(self,instance,validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance