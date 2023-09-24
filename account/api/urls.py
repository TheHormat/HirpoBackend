from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views
app_name = "accounts-api"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify/<id>", views.VerifyView.as_view(), name="verify"),
    path("SendResetCodeView/", views.SendResetCodeView.as_view(), name="SendResetCodeView"),
    path("ChangePasswordVerifyView/<id>", views.ChangePasswordVerifyView.as_view(), name="ChangePasswordVerifyView"),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('EmployeeChangePasswordView/<int:id>',views.EmployeeChangePasswordView.as_view(), name='EmployeeChangePasswordView'),
]
